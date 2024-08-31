import pandas as pd
import numpy as np
import uuid

from Server import Server
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand
from external import *

seeds = known_seeds('test')
time_steps = 168
slotCapacities = [0, 0, 0, 0]
existingServers = [[], [], [], []]

# FILES
demand = pd.read_csv('data/demand.csv')
dataCenters = pd.read_csv('data/datacenters.csv')
servers = pd.read_csv('data/servers.csv')

def get_solution(orgDemand):
    for i in range(1, 10):
        demand = orgDemand[orgDemand['time_step'] == i]
        currentServerGens = demand['server_generation'].values

        print(demand)
        for g in currentServerGens:
            for ls in get_known('latency_sensitivity'):
                info = servers[servers['server_generation'] == g]
                capacity = info['capacity'].values.astype(int)
                slotSize = info['slots_size'].values.astype(int)
                totalUnitCapacity = 0
                demandValue = demand[demand['server_generation'] == g][ls].values.astype(int)
                
                while totalUnitCapacity < demandValue:
                    totalUnitCapacity += capacity
                    maxSlotCapacity = 0
                    index = 0

                    for i, row in dataCenters.iterrows():
                        if row['latency_sensitivity'] == ls:
                            maxSlotCapacity = row['slots_capacity']
                            index = i
                            break                          

                    if slotCapacities[index] + slotSize > maxSlotCapacity:
                        continue

                    s = Server(uuid.uuid4(), g)                    
                    slotCapacities[index] += slotSize
                    existingServers[index].append(s)

    print(slotCapacities)
    pass


for seed in seeds:
    # SET THE RANDOM SEED
    np.random.seed(seed)

    # GET DEMAND
    actual_demand = get_actual_demand(demand)

    # SOLUTION
    solution = get_solution(actual_demand)

    # SAVE SOLUTION
    # save_solution(solution, f'./output/{seed}.json')