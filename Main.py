import numpy as np
import pandas as pd

from DataCentre_Temp import DataCentre
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand

seeds = known_seeds('training')
demandCSV = pd.read_csv('data/demand.csv')
dataCentresCSV = pd.read_csv('data/datacenters.csv')
dataCentres = []

# demand = get_actual_demand(demandCSV)
# print(demand)

for i in range(4):
    c = dataCentresCSV[dataCentresCSV['datacenter_id'] == 'DC' + str(i + 1)]
    print(c['datacenter_id'])




# examp = seeds[0]

# # Numpy.random.seed makes random numbers predictable
# # Everytime the seed is reset with the same seed value, the same set of numbers will be generated

# np.random.seed(examp)
# print(np.random.rand(4))
# np.random.seed(examp)
# print(np.random.rand(4))