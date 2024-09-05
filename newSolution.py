import numpy as np
import pandas as pd
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

# CSV
demandCSV = pd.read_csv('data/demand.csv')

# Known
seeds = known_seeds('test')
latencySensitivities = ['low', 'medium', 'high']
timeSteps = 168

# ------------------------------- DICTIONARY LOGIC
def addToDict(newServers, action, timeStep):
    newServers = newServers.reset_index()

    timeSteps = [timeStep] * len(newServers)
    dcIDs = newServers['datacenter_id']
    generations = newServers['server_generation']
    serverIDs = newServers['server_id']    

    df = pd.DataFrame()
    
    df['time_step'] = timeSteps
    df['datacenter_id'] = dcIDs
    df['server_generation'] = generations
    df['server_id'] = serverIDs
    df['action'] = action

    actions.extend(df.to_dict('records'))
   

# ------------------------------- SERVER LOGIC
def checkExpiration(timeStep):
    for dc in dataCentres:
        s = dc['servers']
        expiredServers = s.loc[s['expire_date'] == timeStep]

        # Check if there are expired servers
        if expiredServers.empty:
            continue
        
        indicies = expiredServers.index
        dc['servers'].drop(indicies, inplace=True)
        addToDict(expiredServers, 'dismiss', timeStep)

def createNewServers(amount, generation, slotSize, timeStep, duration, dcID):
    df = pd.DataFrame()
    IDs = [str(uuid.uuid4()) for x in range(amount)]
    
    df['server_id'] = IDs
    df['datacenter_id'] = dcID
    df['server_generation'] = generation
    df['slot_size'] = slotSize
    df['bought_date'] = timeStep
    df['expire_date'] = timeStep + duration        

    return df

def manage(row):    
    demanded_serverAmountList = []
    current_serverAmountList = []
    timeStep = row['time_step']    

    # Server info
    generation = row['server_generation']        
    releaseRange = literal_eval(Server.getInfo(generation, 'release_time').values.tolist()[0])
    startDate = releaseRange[0]
    endDate = releaseRange[1]
    slotSize = Server.getInfo(generation, 'slots_size').values[0].astype(int)    
    capacity = Server.getInfo(generation, 'capacity').values[0].astype(int)    
    duration = Server.getInfo(generation, 'life_expectancy').values[0].astype(int)

    # Calculate demanded server amount based on demanded generation type
    for ls in latencySensitivities:
        d = row[ls]
        demanded_serverAmountList.append(math.ceil(d / capacity))
    
    # Get current server amount based on demanded generation type
    for ls in latencySensitivities:
        a = 0

        for dcR in dataCentres:
            if dcR['latency_sensitivity'] == ls:
                s = dcR['servers']
                a += len(s.loc[s['server_generation'] == generation])

        current_serverAmountList.append(a)

    diff_serverAmountList = np.subtract(demanded_serverAmountList, current_serverAmountList)    
    diff_serverAmountDF = pd.DataFrame(columns=latencySensitivities)
    diff_serverAmountDF.loc[len(diff_serverAmountDF)] = diff_serverAmountList

    # Check if server is still in its buying range
    if not (startDate <= timeStep <= endDate):
        return
    
    for ls in latencySensitivities:
        remaining_serverAmount = diff_serverAmountDF[ls].values[0].astype(int)
        remaining_slotAmount = remaining_serverAmount * slotSize

        # Check if servers are needed to satisfy demand
        if remaining_serverAmount <= 0:
            continue

        # Buy more servers
        for dc in dataCentres:
            if dc['latency_sensitivity'] == ls:
                dcID = dc['id']
                s = dc['servers']
                usedSlots = s['slot_size'].sum()
                maxSlots = dc['slots_capacity']
                availableSlots = maxSlots - usedSlots

                # If there are not enough slots available, continue
                if availableSlots < slotSize:
                    continue
                
                amount = 0
                if remaining_slotAmount <= availableSlots: # If there are enough available slots to hold the new servers
                    amount = remaining_serverAmount          

                    remaining_serverAmount = 0
                    remaining_slotAmount = 0
                else: # Buy as much servers to meet demand
                    amount = math.floor(availableSlots / slotSize)

                    remaining_serverAmount -= amount
                    remaining_slotAmount -= (amount * slotSize)

                newServers = createNewServers(amount, generation, slotSize, timeStep, duration, dcID)
                dc['servers'] = pd.concat([s, newServers], ignore_index=True) 
                addToDict(newServers, 'buy', timeStep)

                if remaining_serverAmount == 0:
                    break

    # If so, buy servers
    # for ls in latencySensitivities:
    #     remaining_serverAmount = diff_serverAmountDF[ls].values[0].astype(int)
    #     remaining_slotAmount = remaining_serverAmount * slotSize
                
    #     # Check if more servers are needed to satisfy demand
    #     if remaining_serverAmount <= 0:
    #         continue

    #     # Buy more servers
    #     for dc in dataCentres:
    #         if dc['latency_sensitivity'] == ls:
    #             dcID = dc['id']
    #             s = dc['servers']
    #             usedSlots = s['slot_size'].sum()
    #             maxSlots = dc['slots_capacity']
    #             availableSlots = maxSlots - usedSlots

    #             # If there are slots available to buy
    #             if availableSlots < slotSize:
    #                 continue

    #             newServers = pd.DataFrame()
    #             if remaining_slotAmount <= availableSlots:
    #                 newServers = createNewServers(remaining_serverAmount, generation, slotSize, timeStep, duration, dcID)

    #                 remaining_serverAmount = 0
    #                 remaining_slotAmount = 0
    #             else:
    #                 availableServerAmount = math.floor(availableSlots / slotSize)
                    
    #                 newServers = createNewServers(availableServerAmount, generation, slotSize, timeStep, duration, dcID)

    #                 remaining_serverAmount -= availableServerAmount
    #                 remaining_slotAmount -= availableServerAmount * slotSize

    #             dcR['servers'] = pd.concat([dcR['servers'], newServers], ignore_index=True)
    #             addToDict(newServers, 'buy', timeStep)     

    #             if remaining_serverAmount == 0:
    #                 break    
        
        # # Replace old generations of servers with new ones
        # # Check if there are still remaining servers needed to be bought
        # if remaining_serverAmount <= 0:
        #     continue
            
        # generationNumber = int(generation[len(generation) - 1])
        # generationPrefix = generation[:len(generation) - 1]

        # # Check if generation number is 1 as it is the lowest
        # if generationNumber == 1:
        #     continue

        # for dc in dataCentres:
        #     if dc['latency_sensitivity'] == ls:
        #         dcID = dc['id']
        #         s = dc['servers']
        #         maxSlots = dc['slots_capacity']
        #         oldGen = []

        #         for n in range(1, generationNumber):
        #             oldGen.append(generationPrefix + str(n))
                
        #         dismissServers = s.loc[s['server_generation'].isin(oldGen)]
                
        #         # Check if there are old version of the server
        #         if dismissServers.empty:
        #             continue
                    
        #         oldServerAmount = len(dismissServers)
        #         dismissIndicies = dismissServers.index.values.tolist()
        #         amount = 0

        #         if remaining_serverAmount <= oldServerAmount:
        #             amount = remaining_serverAmount

        #             if remaining_serverAmount < oldServerAmount:
        #                 dismissServers = dismissServers[:remaining_serverAmount]
        #                 dismissIndicies = dismissIndicies[:remaining_serverAmount]
                    
        #             remaining_serverAmount = 0
        #             remaining_slotAmount = 0
        #         else:
        #             amount = oldServerAmount

        #             remaining_serverAmount -= oldServerAmount
        #             remaining_slotAmount -= oldServerAmount * slotSize                                

        #         dc['servers'].drop(dismissIndicies, inplace=True)
        #         addToDict(dismissServers, 'dismiss-sell', timeStep)

        #         newServers = createNewServers(amount, generation, slotSize, timeStep, duration, dcID)
        #         dc['servers'] = pd.concat([dc['servers'], newServers], ignore_index=True)
        #         addToDict(newServers, 'buy', timeStep)

        #         if remaining_serverAmount <= 0:
        #             break


def get_solution(actualDemands):
    for t in range(1, timeSteps + 1):        
        demands_t = actualDemands.loc[actualDemands['time_step'] == t]
        
        checkExpiration(t)           
        print(t)
        demands_t.apply(manage, axis=1)        

    return actions

# BEGINNING
for seed in seeds:
    global actions, dataCentres
    actions = []
    dataCentres = createDataCentres(4)

    # Set random seed
    np.random.seed(seed)

    # Get randomized demands
    actualDemands = get_actual_demand(demandCSV)

    # Calculate
    solution = get_solution(actualDemands)

    with open('{}.json'.format(seed), 'w') as fp:
        json.dump(actions, fp)
    print('SEED DONE ->', seed)

print('FINISHED!')

'''
if t == 118:
            dc = dataCentres[3]
            s = dc['servers']
            gs = s.loc[s['server_generation'].isin(['GPU.S1', 'GPU.S2', 'GPU.S3'])]['server_generation'].values.tolist()
            ids = s.loc[s['server_generation'].isin(['GPU.S1', 'GPU.S2', 'GPU.S3'])]['server_id'].values.tolist()

            with open('checkGenerations.json', 'w') as fp:
                json.dump(gs, fp)

            with open('checkIDs.json', 'w') as fp:
                json.dump(ids, fp)
'''