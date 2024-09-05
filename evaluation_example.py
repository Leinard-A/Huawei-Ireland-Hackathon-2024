

from utils import (load_problem_data,
                   load_solution)
from evaluation import evaluation_function

# DEFAULT SEED = 123
# LOAD SOLUTION
solution = load_solution('./output/Training/8933.json')

# LOAD PROBLEM DATA
demand, datacenters, servers, selling_prices = load_problem_data('data/')

# EVALUATE THE SOLUTION
score = evaluation_function(solution,
                            demand,
                            datacenters,
                            servers,
                            selling_prices,
                            seed=8933)

print(f'Solution score: {score}')