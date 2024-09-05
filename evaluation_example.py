import numpy as np

from utils import (load_problem_data,
                   load_solution)
from evaluation import evaluation_function
from seeds import known_seeds

# DEFAULT SEED = 123
# LOAD SOLUTION
fileName = '4201.json'
solution = load_solution(fileName)

# LOAD PROBLEM DATA
demand, datacenters, servers, selling_prices = load_problem_data('data/')

# EVALUATE THE SOLUTION
fileSeed = int(fileName.split('.')[0])

score = evaluation_function(solution,
                            demand,
                            datacenters,
                            servers,
                            selling_prices,
                            seed=fileSeed)

print(score)
