import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import truncweibull_min
import uuid
import json
import math

# Class import
import Server

# Function import
from seeds import known_seeds
from evaluation import get_actual_demand
from ast import literal_eval
from DataCentre import createDataCentres
from known import getKnown
from profit import findRevenue

# CSV
demandCSV = pd.read_csv('data/demand.csv')

# Known
seeds = known_seeds('test')
latencySensitivities = getKnown('ls')
timeSteps = getKnown('timeStep')
order = True

# ------------ DICTIONARY LOGIC
def actionDict(servers, action, timeStep):
    servers = servers.reset_index(drop=True)

    timeSteps = [timeStep] * len(servers)
    dcIDs = servers['datacenter_id']
    generations = servers['server_generation']
    serverIDs = servers['server_id']    

    df = pd.DataFrame()
    
    df['time_step'] = timeSteps
    df['datacenter_id'] = dcIDs
    df['server_generation'] = generations
    df['server_id'] = serverIDs
    df['action'] = action

    return df.to_dict('records')

# ------------ SERVER LOGIC
def adjustFailure(capacity):
    return int(capacity * (1 - truncweibull_min.rvs(0.3, 0.05, 0.1, size=1)).item())

def orderBy(demand_t, mode):
    newDF = demand_t.copy()

    if mode == 'genType':
        genOrder = demand_t['server_generation'].values.tolist()
        genNums = [0] * len(genOrder)

        for i, g in enumerate(genOrder):
            genNums[i] = int(g.split('.')[1][1])
        
        newDF['GenNums'] = genNums
        newDF = newDF.sort_values(by=['GenNums'], ascending=False)
        newDF.drop(columns=['GenNums'], inplace=True)
    elif mode == 'totalDemand':
        totals = []

        for i, g in demand_t.iterrows():            
            t = g['low'] + g['medium'] + g['high']

            totals.append(t)
        
        newDF['TotalDemand'] = totals
        newDF = newDF.sort_values(by=['TotalDemand'], ascending=False)
        newDF.drop(columns=['TotalDemand'], inplace=True)

    return newDF

def checkExpiration(timeStep):
    for dc in datacentres:
        s = dc['servers']
        expiredServers = s.loc[s['expire_date'] == timeStep]

        # Check if there are no expired servers
        if expiredServers.empty:
            continue
            
        i = expiredServers.index
        dc['servers'].drop(i, inplace=True)
        dc['servers'] = dc['servers'].reset_index(drop=True)
        actions.extend(actionDict(expiredServers, 'dismiss', timeStep))

# Converts given IDs to a data frame format used in datacentres
def toDF(IDs, generation, slotSize, duration, timeStep, dcID):
    df = pd.DataFrame()    

    df['server_id'] = IDs
    df['datacenter_id'] = dcID
    df['server_generation'] = generation
    df['slot_size'] = slotSize
    df['buy_date'] = timeStep
    df['expire_date'] = timeStep + duration

    return df

def satisfy(row):
    demanded_serverAmountList = [] # ['low', 'medium', high]
    current_serverAmountList = [] # ['low', 'medium', high]
    timeStep = row['time_step']

    # Server info
    generation = row['server_generation']        
    releaseRange = literal_eval(Server.getInfo(generation, 'release_time').values.tolist()[0])
    startDate = releaseRange[0]
    endDate = releaseRange[1]
    slotSize = Server.getInfo(generation, 'slots_size').values[0].astype(int)    
    capacity = Server.getInfo(generation, 'capacity').values[0].astype(int)    
    duration = Server.getInfo(generation, 'life_expectancy').values[0].astype(int)

    # Calculate demanded server amount for each latency sensitivity based on generation
    for ls in latencySensitivities:
        d = row[ls]
        demanded_serverAmountList.append(math.ceil(d / capacity))

    # Get current server amount for each latency sensitivity based on generaion
    for ls in latencySensitivities:
        a = 0

        for dc in datacentres:
            if dc['latency_sensitivity'] == ls:
                s = dc['servers']
                a += len(s.loc[s['server_generation'] == generation])

        current_serverAmountList.append(a)
    
    # Find how many more servers are needed to satisfy demand based on the current amount of servers
    a_sD = np.subtract(demanded_serverAmountList, current_serverAmountList) # ACTUAL SERVER DEMAND    
    actualDF = pd.DataFrame(columns=latencySensitivities)
    actualDF.loc[len(actualDF)] = a_sD

    # Check if server can be bought
    if not startDate <= timeStep <= endDate:
        return
    
    for ls in latencySensitivities:
        a_dSA = actualDF[ls].values[0].astype(int) # Actual Demanded Server Amount
                
        if a_dSA > 0: # If value is positive, buy more servers to try and meet demand
            r_dASA = a_dSA # Remaining Actual Demanded Server Amount

            dcInd = []
            # Find datacentres with the same latency sensitivity
            for i, dc in enumerate(datacentres):
                if dc['latency_sensitivity'] == ls:
                    dcInd.append(i)
            
            # Iterate through the datacentres
            for i in dcInd:
                dc = datacentres[i]
                dcID = dc['ID']
                s = dc['servers']
                usedSlots = s['slot_size'].sum()
                maxCapacity = dc['slots_capacity']
                availableSlots = maxCapacity - usedSlots
                availableServerAmount = math.floor(availableSlots / slotSize)

                if availableServerAmount <= 0:
                    continue

                amount = 0
                if r_dASA <= availableServerAmount: # If there are enough slots to buy and meet demand in current data centre
                    amount = r_dASA

                    r_dASA = 0
                else: # Buy as much servers as possible to try and meet demand in current centre
                    amount = availableServerAmount

                    r_dASA -= availableServerAmount
                
                newServers = toDF([str(uuid.uuid4()) for x in range(amount)], generation, slotSize, duration, timeStep, dcID)
                datacentres[i]['servers'] = pd.concat([datacentres[i]['servers'], newServers], ignore_index=True)
                actions.extend(actionDict(newServers, 'buy', timeStep))
                actionedServers.extend(newServers['server_id'].values.tolist())
                
                # Check if there are no more servers needed to be bought
                if r_dASA <= 0:
                    break
            
            # After buying, check if all servers were bought to meet demand, if not replace old generations
            if r_dASA <= 0:
                continue

            generationNumber = int(generation.split('.')[1][1])
            generationPrefix = generation[:len(generation) - 1]

            # If generation nubmer is 1, move on as 1 is the oldest generation
            if generationNumber == 1:
                continue

            # Get old generations of current generation
            oldGens = []
            for n in range(1, generationNumber):
                oldGens.append(generationPrefix + str(n))

            dcInd = []
            # Find datacentres with the same latency sensitivity
            for i, dc in enumerate(datacentres):
                if dc['latency_sensitivity'] == ls:
                    dcInd.append(i)

            # Iterate
            for i in dcInd:
                dc = datacentres[i]
                dcID = dc['ID']
                s = dc['servers']
                oldServers = s.loc[s['server_generation'].isin(oldGens) & ~s['server_id'].isin(actionedServers)]
                oldServerAmount = len(oldServers)
                
                # Check if there are no old servers
                if oldServerAmount <= 0:
                    continue

                amount = 0
                if r_dASA <= oldServerAmount: # If there are enough old servers, upgrade
                    amount = r_dASA

                    r_dASA = 0
                else: # Upgrade as much servers as possible
                    amount = oldServerAmount

                    r_dASA -= oldServerAmount
                
                dismissedServers = oldServers[:amount]
                dismissedIndicies = dismissedServers.index.values.tolist()

                # Dismiss the old generation servers
                datacentres[i]['servers'].drop(dismissedIndicies, inplace=True)
                dismissedServers = toDF(dismissedServers['server_id'], dismissedServers['server_generation'], dismissedServers['slot_size'], dismissedServers['expire_date'], timeStep, dcID)
                actions.extend(actionDict(dismissedServers, 'dismiss', timeStep))

                # Buy the newest server
                newServers = toDF([str(uuid.uuid4()) for x in range(amount)], generation, slotSize, duration, timeStep, dcID)
                datacentres[i]['servers'] = pd.concat([datacentres[i]['servers'], newServers], ignore_index=True)
                actions.extend(actionDict(newServers, 'buy', timeStep))
                
                '''
                    Adds the new servers to a list called 'actionedServers'
                    The purpose is to stop servers from having more than 1 action during the turn.
                    When going through each row of the demand at a time step, multiple generations of a type will be demanded.
                    The oldest one will go first -> buying as much servers as possible to meet demand and then upgrade old servers aswell.
                    Then the next row of the demand is a newer version and without this it will dismiss the servers that were just bought at the same time step.
                    Can not have more than 1 action for each server at each time step 
                '''
                actionedServers.extend(newServers['server_id'].values.tolist())



def get_solution(demand):
    for t in range(1, timeSteps + 1):
        global actionedServers
        actionedServers = []
        # Check for expired servers at current time step
        checkExpiration(t)
        
        # Server logic        
        print(t)
        demand_t = demand.loc[demand['time_step'] == t]
        demand_t = orderBy(demand_t, 'genType')
        demand_t.apply(satisfy, axis=1)        

    
    return actions

for seed in seeds:
    global actions, datacentres
    actions = []
    datacentres = createDataCentres()

    # Set random seed
    np.random.seed(seed)

    # Randomize demand
    demand = get_actual_demand(demandCSV)    

    # Calculate
    solution = get_solution(demand)    

    with open('{}.json'.format(seed), 'w') as fp:
        json.dump(actions, fp)
    print('SEED DONE ->', seed)