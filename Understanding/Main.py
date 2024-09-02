import pandas as pd
import numpy as np
import math
import uuid
import json

from Server import Server
from DataCentre_Temp import DataCentre

from seeds import known_seeds
from evaluation import get_actual_demand
from external import createDataCentres
from external import get_known
from ast import literal_eval


seeds = known_seeds('training')
timeSteps = get_known('time_steps')
dataCentres = createDataCentres()
usedSlots = [0, 0, 0, 0]
actions = []

# CSVS
demandCSV = pd.read_csv('data/demand.csv')
dataCentreCSV = pd.read_csv('data/datacenters.csv')


def actionDFtoDict(IDs, timeSteps, datacenterIDs, serverGenerations, action):
    df = pd.DataFrame()

    df['ID'] = IDs
    df['time_step'] = timeSteps
    df['datacenter_id'] = datacenterIDs
    df['server_generation'] = serverGenerations

    df.apply(addAction, action=action, axis=1)

def addAction(row, action):
    if np.isnan(row['time_step']): 
        return

    dic = {
        'time_step': row['time_step'],
        'datacenter_id': row['datacenter_id'],
        'server_generation': row['server_generation'],
        'server_id': row['ID'],
        'action': action
    }

    actions.append(dic)

def checkLife(timeStep):
    for dI in range(len(dataCentres)):
        dc = dataCentres[dI]
        times = dc.loc[dc['expiration_time_step'] == timeStep] 

        if not times.empty:            
            actionDFtoDict(times['ID'], timeStep, dc.Name, times['server_generation'], 'sell')

            totalSlots = times['slot_size'].sum()
            usedSlots[dI] -= totalSlots
            dataCentres[dI].drop(times.index, inplace=True)

def buy(row):
    generation = row['server_generation']
    timeStep = row['time_step']
    releaseDate = literal_eval(Server.getInfo(generation, 'release_time').values.tolist()[0])
    capacity = int(Server.getInfo(generation, 'capacity').values[0])
    slotSize = int(Server.getInfo(generation, 'slots_size').values[0])
    lifeExp = int(Server.getInfo(generation, 'life_expectancy').values[0])

    if releaseDate[0] <= timeStep <= releaseDate[1]:
        for ls in get_known('latency_sensitivity'):
            demand = row[ls]
            amount = math.ceil(demand / capacity)
            dcInfo = dataCentreCSV.loc[dataCentreCSV['latency_sensitivity'] == ls]
            dcIndices = dcInfo.index

            for i in dcIndices:
                dc = dataCentres[i]
                name = dc.Name

                maxCapacity = int(DataCentre.getInfo('DC' + str(i + 1), 'slots_capacity').values[0])
                totalSlotSize = amount * slotSize

                if usedSlots[i] + totalSlotSize <= maxCapacity:
                    usedSlots[i] += totalSlotSize
                    df = pd.DataFrame()                    
                    IDs = [str(uuid.uuid4()) for id in range(amount)]

                    actionDFtoDict(IDs, timeStep, name, generation, 'buy') 

                    df['ID'] = IDs
                    df['server_generation'] = generation
                    df['slot_size'] = slotSize
                    df['bought_at_time_step'] = timeStep
                    df['expiration_time_step'] = timeStep + lifeExp                                                  

                    dataCentres[i] = pd.concat([dc, df], ignore_index=True)
                    dataCentres[i].Name = name
                    break


def get_solution(demand):    
    for i in range(1, timeSteps):
        checkLife(i)
        currentDemand = demand.loc[demand['time_step'] == i]
        currentDemand.apply(buy, axis=1)    
    
    return actions

# SET THE RANDOM SEED
index = 0
for seed in seeds:
    actions = []
    np.random.seed(seed)

    # GET ACTUAL DEMANDS
    actualDemands = get_actual_demand(demandCSV)

    # SOLUTION
    solution = get_solution(actualDemands)
    
    with open('solution{}.json'.format(index + 1), 'w') as fp:
        json.dump(actions, fp)
        
    index += 1

print('DONE')