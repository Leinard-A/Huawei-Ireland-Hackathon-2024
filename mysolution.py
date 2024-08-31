
import numpy as np
import pandas as pd
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand
##Additional Libraries
import dataCentClass as DC 
import serverClass as SC



def get_my_solution(d):
    ##Getting Data from CSV files
    serverList = pd.read_csv('./data/servers.csv')
    print(serverList)
    dataCentreList = pd.read_csv('./data/datacenters.csv')
    ##Inserts CSV data into class structures
    DC1D = dataCentreList[dataCentreList['datacenter_id'] == 'DC1'].values
    DC1D = DC1D[0]
    DC2D = dataCentreList[dataCentreList['datacenter_id'] == 'DC2'].values
    DC2D = DC2D[0]
    DC3D = dataCentreList[dataCentreList['datacenter_id'] == 'DC3'].values
    DC3D = DC3D[0]
    DC4D = dataCentreList[dataCentreList['datacenter_id'] == 'DC4'].values
    DC4D = DC4D[0]
    ##Initialising Data Centres 
    DC1 = DC.DataCentre(DC1D[0],
        DC1D[1],
        DC1D[2],
        DC1D[3]            
    )
    DC2 = DC.DataCentre(DC2D[0],
        DC2D[1],
        DC2D[2],
        DC2D[3]                    
    )
    DC3 = DC.DataCentre(DC3D[0],
        DC3D[1],
        DC3D[2],
        DC3D[3]
    )
    DC4 = DC.DataCentre(DC4D[0],
        DC4D[1],
        DC4D[2],
        DC4D[3]                    
    )

    for i in range(int((d['time_step'].count()/2))):
        time_stepDemand = d[d['time_step']== i+1].values
        currentDemand = {}
        for items in range(len(time_stepDemand)):
            print(time_stepDemand[items])
            currentDemand['highDemand'] = time_stepDemand[items][2]
            currentDemand['lowDemand'] = time_stepDemand[items][3]
            currentDemand['mediumDemand'] = time_stepDemand[items][4]

        ##Then Process the demand data and have it in a stored format
        ##This is the area where the decision making goes- Leinard








        ##End of turn 
        DC1.nextTurn()
        DC2.nextTurn()
        DC3.nextTurn()
        DC4.nextTurn()
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

