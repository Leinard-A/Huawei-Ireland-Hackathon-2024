import numpy as np
import pandas as pd
import os

from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand

seeds = known_seeds('training')
demand = pd.read_csv('data/demand.csv')


# SET SEED
np.random.seed(seeds[0])

# GET DEMAND
actual_demand = get_actual_demand(demand)

print(actual_demand)










# examp = seeds[0]

# # Numpy.random.seed makes random numbers predictable
# # Everytime the seed is reset with the same seed value, the same set of numbers will be generated

# np.random.seed(examp)
# print(np.random.rand(4))
# np.random.seed(examp)
# print(np.random.rand(4))