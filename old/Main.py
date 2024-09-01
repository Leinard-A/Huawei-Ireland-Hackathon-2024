import pandas as pd
import numpy as np
import uuid
import math

from Server import Server
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand
from external import *

seeds = known_seeds('test')
time_steps = 168
dataCentres = createDataCentres()

# FILES
demandCSV = pd.read_csv('data/demand.csv')
dataCentresCSV = pd.read_csv('data/datacenters.csv')
serversCSV = pd.read_csv('data/servers.csv')


def updateServerLife(currentTimeStep):
    for d in dataCentres:
        for s in d.servers:
            s.checkLife(currentTimeStep)


def buyServers(demand, demandedGenerations, currentTimeStep):
    for g in demandedGenerations:
        for ls in get_known('latency_sensitivity'):
            info = serversCSV[serversCSV['server_generation'] == g]
            capacity = info['capacity'].values[0]      
            slotSize = info['slots_size'].values[0]
            demandValue = demand[demand['server_generation'] == g][ls].values[0]     
            dcInfo = dataCentresCSV[dataCentresCSV['latency_sensitivity'] == ls]
            dcIndex = dcInfo.index               
            serverAmount = math.ceil(demandValue / capacity)
            usedSlots = serverAmount * slotSize

            for ind in dcIndex: # A for loop due to being 2 high latency sensitivity servers
                if usedSlots < dataCentres[ind].slotCapacity - usedSlots:
                    for a in range(serverAmount):
                        s = Server(uuid.uuid4(), g, currentTimeStep)                                           
                        dataCentres[ind].addServer(s)
                    break  


def get_solution(orgDemand):
    for i in range(1, 20):
        demand = orgDemand[orgDemand['time_step'] == i]
        demandedGenerations = demand['server_generation'].values

        print('-----')
        updateServerLife(i)
        buyServers(demand, demandedGenerations, i)

                              

    pass


for seed in seeds:
    # SET THE RANDOM SEED
    np.random.seed(seed)

    # GET DEMAND
    actual_demand = get_actual_demand(demandCSV)

    # SOLUTION
    solution = get_solution(actual_demand)

    # SAVE SOLUTION
    # save_solution(solution, f'./output/{seed}.json')