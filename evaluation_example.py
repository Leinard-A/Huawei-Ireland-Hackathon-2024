import numpy as np

from utils import (load_problem_data,
                   load_solution)
from evaluation import evaluation_function
from seeds import known_seeds

# DEFAULT SEED = 123
# LOAD SOLUTION
seeds = known_seeds('actual')
m_seed = '2281'

fileName = '{}.json'.format(m_seed)
solution = load_solution(fileName)

# LOAD PROBLEM DATA
demand, datacenters, servers, selling_prices = load_problem_data('data/')

# EVALUATE THE SOLUTION
score = evaluation_function(solution,
                            demand,
                            datacenters,
                            servers,
                            selling_prices,
                            seed=m_seed)

print(m_seed, score)
