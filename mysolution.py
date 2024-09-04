import numpy as np
import pandas as pd
import math
import uuid
import json

# Class importing
import Server
from DataCentre import createDataCentres

# Function importing
from seeds import known_seeds
from evaluation import get_actual_demand
from ast import literal_eval

# CSV
demandCSV = pd.read_csv('data/demand.csv')

# Known
seeds = known_seeds('training')
latencySensitivities = ['low', 'medium', 'high']
timeSteps = 168

# Variables
global actions, dataCentres

# DICTIONARY LOGIC
def addAction(row, action):
    if np.isnan(row['time_step']):
        return

    dict = {
        'time_step': row['time_step'],
        'datacenter_id': row['datacenter_id'],
        'server_generation': row['server_generation'],
        'server_id': row['ID'],
        'action': action
    }

    actions.append(dict)

def addToDict(IDs, timeStep, dcID, generation, action):    
    df = pd.DataFrame()

    df['ID'] = IDs
    df['time_step'] = timeStep
    df['datacenter_id'] = dcID
    df['server_generation'] = generation

    df.apply(addAction, action=action, axis=1)

    
# SERVER LOGIC
def checkExpiration(timeStep):
    for dc in dataCentres:
        servers = dc['servers']
        expiredServers = servers.loc[servers['expire_date'] == timeStep]

        # Check if there are expired servers
        if expiredServers.empty:
            continue
        
        addToDict(expiredServers['server_id'], timeStep, dc['id'], expiredServers['server_generation'], 'dismiss')

        indices = expiredServers.index
        dc['servers'].drop(indices, inplace=True)

def createNewServers(amount, generation, slotSize, timeStep, lifeExp, dcID):
    df = pd.DataFrame()
    IDs = [str(uuid.uuid4()) for x in range(amount)]

    df['server_id'] = IDs
    df['server_generation'] = generation
    df['slot_size'] = slotSize
    df['bought_date'] = timeStep
    df['expire_date'] = timeStep + lifeExp    

    return df

def manage(row):
    generation = row['server_generation']
    timeStep = row['time_step']

    for ls in latencySensitivities:
        serverAmount = 0

        # Find data centre with matching latency sensitivity
        for dc in dataCentres:
            if dc['latency_sensitivity'] == ls:
                servers = dc['servers']
                serverAmount += len(servers.loc[servers['server_generation'] == generation])                

        # Server info based on generation
        capacity = Server.getInfo(generation, 'capacity').values[0].astype(int)
        slotSize = Server.getInfo(generation, 'slots_size').values[0].astype(int)
        lifeExp = Server.getInfo(generation, 'life_expectancy').values[0].astype(int)
        releaseRange = literal_eval(Server.getInfo(generation, 'release_time').values.tolist()[0])
        startDate = releaseRange[0]
        endDate = releaseRange[1]

        # Calculate server amount
        demand = row[ls]
        d_serverAmount = math.ceil(demand / capacity)
        d_slotAmount = d_serverAmount * slotSize

        # Gets actual demand based off previous records
        d_serverAmount = d_serverAmount - serverAmount
        d_slotAmount = d_slotAmount - (serverAmount * slotSize)

        # Check if server generation can be bought with its release date
        if not (startDate <= timeStep <= endDate):
            continue

        # If the demand is more than previous, buy more
        if d_serverAmount > 0:
            remainingServerAmount = d_serverAmount # For dictionary creation
            remainingSlotAmount = d_slotAmount # For logic      
            full = True

            '''
                Iterate through each data centre fill them with servers to meet demand.
                
                Will fill a data centre with as much servers as possible to satisfy demand and any remaining servers will be bought in a different data centre
                with the same latency sensitivity to satisfy demand.
            '''
            # BUY NEW SERVERS
            for iDC in dataCentres:
                if iDC['latency_sensitivity'] == ls:
                    iServers = iDC['servers']
                    iUsedSlots = iServers['slot_size'].sum()
                    iMaxCapacity = iDC['slots_capacity']
                    iAvailableSlots = iMaxCapacity - iUsedSlots

                    # Check if there are enough available slots to buy new servers
                    if iAvailableSlots <= 0:
                        continue
                    
                    full = False
                    # Buy as much servers as possible to try and satisfy demand
                    if remainingSlotAmount > iAvailableSlots:
                        iAvailableServerAmount = math.floor(iAvailableSlots / slotSize)
                        if iAvailableServerAmount <= 0:
                            continue

                        newServers = createNewServers(iAvailableServerAmount, generation, slotSize, timeStep, lifeExp, iDC['id'])
                        iDC['servers'] = pd.concat([iServers, newServers], ignore_index=True)
                        addToDict(newServers['server_id'], timeStep, iDC['id'], newServers['server_generation'], 'buy')

                        remainingServerAmount -= iAvailableServerAmount
                        remainingSlotAmount -= (iAvailableServerAmount * slotSize)
                    else: # Buy servers to meet demand                                                     
                        newServers = createNewServers(remainingServerAmount, generation, slotSize, timeStep, lifeExp, iDC['id'])
                        iDC['servers'] = pd.concat([iServers, newServers], ignore_index=True)
                        addToDict(newServers['server_id'], timeStep, iDC['id'], newServers['server_generation'], 'buy')

                        remainingServerAmount = 0
                        remainingSlotAmount = 0
                        break
            
            # REPLACE OLD GENERATIONS
            if remainingServerAmount > 0:
                full = True
            
            if not full:
                continue

            generationNumber = int(generation[len(generation) - 1])
            generationPrefix = generation[:len(generation) - 1]

            if generationNumber == 1:
                continue
            
            for iDC in dataCentres:
                if iDC['latency_sensitivity'] == ls:
                    iServers = iDC['servers']
                    iMaxCapacity = iDC['slots_capacity']
                    oldServersDF = pd.DataFrame()
                    oldServerIndicies = []
                    oldGenerations = []

                    for n in range(1, generationNumber):
                        oldGenerations.append(generationPrefix + str(n))
                    
                    oldServers = iServers.loc[iServers['server_generation'].isin(oldGenerations)]                        
                    oldServersDF = pd.concat([oldServersDF, oldServers], ignore_index=True)
                    oldServerIndicies += oldServers.index.values.tolist()

                    if oldServersDF.empty:
                        continue

                    oldServerAmount = len(oldServerIndicies)
                    oldSlotAmount = oldServersDF['slot_size'].sum()

                    if remainingServerAmount < oldServerAmount:
                        iDC['servers'].drop(oldServerIndicies[:remainingServerAmount], inplace=True)
                        addToDict(oldServers['server_id'][:remainingServerAmount], timeStep, iDC['id'], oldServers['server_generation'][:remainingServerAmount], 'dismiss')

                        newServers = createNewServers(remainingServerAmount, generation, slotSize, timeStep, lifeExp, iDC['id'])
                        iDC['servers'] = pd.concat([iDC['servers'], newServers], ignore_index=True)
                        addToDict(newServers['server_id'], timeStep, iDC['id'], newServers['server_generation'], 'buy')

                        remainingServerAmount = 0
                        remainingSlotAmount = 0
                        break
                    else:
                        iDC['servers'].drop(oldServerIndicies, inplace=True)
                        addToDict(oldServers['server_id'], timeStep, iDC['id'], oldServers['server_generation'], 'dismiss')

                        newServers = createNewServers(oldServerAmount, generation, slotSize, timeStep, lifeExp, iDC['id'])
                        iDC['servers'] = pd.concat([iDC['servers'], newServers], ignore_index=True)
                        addToDict(newServers['server_id'], timeStep, iDC['id'], newServers['server_generation'], 'buy')

                        remainingServerAmount -= oldServerAmount
                        remainingSlotAmount -= oldSlotAmount
                                
def get_solution(actualDemands):       
    for t in range(1, timeSteps):
        timeStepDemands = actualDemands.loc[actualDemands['time_step'] == t]

        # Management
        checkExpiration(t)
        timeStepDemands.apply(manage, axis=1)        

    return actions

for seed in seeds:    
    actions = []
    dataCentres = createDataCentres(4)

    # SET RANDOM SEED
    np.random.seed(seed)

    # GET RANDOMIZED DEMANDS
    actualDemands = get_actual_demand(demandCSV)

    # CALCULATE
    solution = get_solution(actualDemands)

    with open('{}.json'.format(seed), 'w') as fp:
        json.dump(solution, fp)

print('DONE!')