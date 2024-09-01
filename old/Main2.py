import pandas as pd
import numpy as np
import uuid
import math

from Server import Server
from DataCentre_Temp import DataCentre

from seeds import known_seeds
from evaluation import get_actual_demand
from external import *

seeds = known_seeds('test')
timeSteps = 168
dataCentres = createDataCentres()

# CSVS
demandCSV = pd.read_csv('data/demand.csv')
serversCSV = pd.read_csv('data/servers.csv')
dataCentresCSV = pd.read_csv('data/datacenters.csv')


def buy(row):
    generation = row['server_generation']
    timeStep = int(row['time_step'])    
    capacity = Server.getInfo(generation, 'capacity')
    slotSize = Server.getInfo(generation, 'slots_size')

    for ls in get_known('latency_sensitivity'):
        demand = row[ls]
        amount = math.ceil(demand / capacity)
        
        dc = dataCentresCSV[dataCentresCSV['latency_sensitivity'] == ls]
        dcIndex = dc.index 
        for i in dcIndex:
            d = dataCentres[i]

            maxCapacity = int(DataCentre.getInfo('DC' + str(i + 1), 'slots_capacity'))
            totalSlotSize = amount * slotSize
            if totalSlotSize < (maxCapacity - totalSlotSize):
                
            # if totalSlotSize < maxCapacity - totalSlotSize:
            #     df = pd.DataFrame()
            #     df['ID'] = [str(uuid.uuid4()) for i in range(amount)]
            #     df['server_generation'] = generation
            #     df['bought_at_time_step'] = timeStep
            #     d = pd.concat([d, df], ignore_index=True)
            #     dataCentres[i] = d
            #     break
        
                


def get_solution(demand):
    for i in range(1, 50):
        currentDemand = demand.loc[demand['time_step'] == i]
        currentDemand.apply(buy, axis=1)
        
    print(dataCentres)
        
        
            
                


# SET THE RANDOM SEED
np.random.seed(seeds[0])

# GET DEMAND
actualDemands = get_actual_demand(demandCSV)

# SOLUTION
solution = get_solution(actualDemands)