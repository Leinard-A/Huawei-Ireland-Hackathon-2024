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

centers = []
slotCapacities = []

for x in dataCentresCSV.values:
    center = DataCentre(x[0], x[1], x[2], x[3])
    centers.append(center) # (Data Center, Used Up Capacity)
    slotCapacities.append([0, x[3]])


def get_my_solution(d):
    totalTimeSteps = get_known('time_steps')
    # for i in range(totalTimeSteps):
    for i in range(totalTimeSteps):
        demandAtTime = d[d['time_step'] == i]
        generations = demandAtTime['server_generation'].values # Processor Units        

        for g in generations:
            for ls in get_known('latency_sensitivity'):
                info = serversCSV[serversCSV['server_generation'] == g]
                capacity = info['capacity'].values.astype(int)
                slotSize = info['slots_size'].values.astype(int)
                serverAmount = 0
                totalUnit = 0
                demand = demandAtTime[demandAtTime['server_generation'] == g]
                demand = demand[ls].values.astype(int)
                
                while totalUnit < demand - capacity:
                    totalUnit += capacity
                    serverAmount += 1                                
                
                for c in range(len(centers)):
                    if (centers[c].latencySensitivity == ls):                    
                        slotCapacities[c][0] += serverAmount * slotSize
                        break 


    print('--------------')                            
    for i in range(len(slotCapacities)):
        print(slotCapacities[i][0], centers[i].ID, centers[i].latencySensitivity)   

    print('--------------')                            
    print(demandAtTime)
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