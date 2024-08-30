import numpy as np
import pandas as pd

from DataCentre_Temp import DataCentre
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand
from evaluation import get_known
from evaluation import get_time_step_demand

seeds = known_seeds('training')
demandCSV = pd.read_csv('data/demand.csv')
dataCentresCSV = pd.read_csv('data/datacenters.csv')
serversCSV = pd.read_csv('data/servers.csv')

dataCenters = []

for x in dataCentresCSV.values:
    center = DataCentre(x[0], x[1], x[2], x[3])
    dataCenters.append(center)


def get_my_solution(d):
    totalTimeSteps = get_known('time_steps')
    # for i in range(totalTimeSteps):
    demandAtTime = d[d['time_step'] == 1]
    procUnits = demandAtTime['server_generation'].values # Processor Units
    print(demandAtTime)

    for unit in procUnits:
        for ls in get_known('latency_sensitivity'):
            unitInfo = serversCSV[serversCSV['server_generation'] == unit]
            capacity = unitInfo['capacity'].values.astype(int)
            serverAmount = 0
            totalUnit = 0
            demand = demandAtTime[demandAtTime['server_generation'] == unit]
            demand = demand[ls].values.astype(int)

            while totalUnit < demand - capacity:
                totalUnit += capacity
                serverAmount += 1
            
                            
        
    return [{}]


# SET RANDOM SEED
np.random.seed(seeds[0])

# GET ACTUAL DEMAND
demand = get_actual_demand(demandCSV)

# CALL YOUR APPROACH HERE
solution = get_my_solution(demand)


# examp = seeds[0]

# # Numpy.random.seed makes random numbers predictable
# # Everytime the seed is reset with the same seed value, the same set of numbers will be generated

# np.random.seed(examp)
# print(np.random.rand(4))
# np.random.seed(examp)
# print(np.random.rand(4))