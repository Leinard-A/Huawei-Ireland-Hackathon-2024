
import numpy as np
import pandas as pd
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand
import ClassObjects as dataObject

def get_my_solution(d):
    ##Inititalise data centre objects
    DC1 = dataObject.DataCentre('DC1')
    DC2 = dataObject.DataCentre('DC2')
    DC3 = dataObject.DataCentre('DC3')
    DC4 = dataObject.DataCentre('DC4')
    ##Filehandeling section to gather info from csv files 
    ##About the Data Centres 


    ##Then the logic section

    return [{}]


seeds = known_seeds('training')

demand = pd.read_csv('./data/demand.csv')
for seed in seeds:
    # SET THE RANDOM SEED
    np.random.seed(seed)

    # GET THE DEMAND
    actual_demand = get_actual_demand(demand)

    # CALL YOUR APPROACH HERE
    solution = get_my_solution(actual_demand)

    # SAVE YOUR SOLUTION
    save_solution(solution, f'./output/{seed}.json')

