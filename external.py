import pandas as pd
import numpy as np
import scipy as sp

dataCentresCSV = pd.read_csv('data/datacenters.csv')

def get_known(key):
    # STORE SOME CONFIGURATION VARIABLES
    if key == 'datacenter_id':
        return ['DC1', 
                'DC2', 
                'DC3', 
                'DC4']
    elif key == 'actions':
        return ['buy',
                'hold',
                'move',
                'dismiss']
    elif key == 'server_generation':
        return ['CPU.S1', 
                'CPU.S2', 
                'CPU.S3', 
                'CPU.S4', 
                'GPU.S1', 
                'GPU.S2', 
                'GPU.S3']
    elif key == 'latency_sensitivity':
        return ['high', 
                'medium', 
                'low']
    elif key == 'required_columns':
        return ['time_step', 
                'datacenter_id', 
                'server_generation', 
                'server_id',
                'action']
    elif key == 'time_steps':
        return 168
    elif key == 'datacenter_fields':
        return ['datacenter_id', 
                'cost_of_energy',
                'latency_sensitivity', 
                'slots_capacity']

def createDataCentres():
    dfs = []
    for n in range(0, 4):
        df = pd.DataFrame(columns=['ID', 'server_generation', 'slot_size', 'bought_at_time_step', 'expiration_time_step'])
        df.Name = 'DC' + str(n + 1)
        dfs.append(df)
    
    return dfs
