import numpy as np
import pandas as pd
import math
import uuid

# Class importing
from Server import Server
from DataCentre import createDataCentres

# Function importing
from seeds import known_seeds
from evaluation import get_actual_demand
from ast import literal_eval

# CVS Handling
demandCSV = pd.read_csv('data/demand.csv')

# Known information
seeds = known_seeds('test')
latencySensitivities = ['low', 'medium', 'high']
totalTimeSteps = 168

# Variables
dataCentres = createDataCentres(4)

def buy(row):    
    generation = row['server_generation']
    timeStep = row['time_step']
    releaseRange = literal_eval(Server.getInfo(generation, 'release_time').values.tolist()[0])
    startDate = releaseRange[0]
    endDate = releaseRange[1]    

    # Checks if server can be bought depending on its release time
    if startDate <=  timeStep <= endDate:        
        for ls in latencySensitivities:
            # Find data centre matching latency sensitivity and add servers
            for dc in dataCentres:
                if dc['latency_sensitivity'] == ls:
                    usedSlots = dc['servers']['slot_size'].sum()
                    maxCapacity = dc['slots_capacity']
                    currentServerAmount = len(dc['servers'].loc[dc['servers']['server_generation'] == generation]) # Get the amount of a specific server generation in the data centre
                    demand = row[ls] # The demand for processors based on latency sensitivity
                    capacity = Server.getInfo(generation, 'capacity').values[0].astype(int) # The amount of processors in a server based on a server generation 
                    slotSize = Server.getInfo(generation, 'slots_size').values[0].astype(int)              
                    lifeExp = Server.getInfo(generation, 'life_expectancy').values[0].astype(int)

                    serverAmount = math.ceil(demand / capacity) # Calculate server amount needed to cover for demand            
                    serverAmount = serverAmount - currentServerAmount if serverAmount > currentServerAmount else 0 # Change server amount if the current demanded servers is bigger than the current amount of servers
                    totalSlotSize = serverAmount * slotSize # Calculate slot amount needed to hold servers

                    if serverAmount == 0:
                        break

                    # Check if there is enough slots available
                    if usedSlots + totalSlotSize < maxCapacity:
                        df = pd.DataFrame()

                        df['server_id'] = [str(uuid.uuid4()) for x in range(serverAmount)]
                        df['server_generation'] = generation
                        df['slot_size'] = slotSize
                        df['bought_date'] = timeStep
                        df['expire_date'] = timeStep + lifeExp

                        dc['servers'] = pd.concat([dc['servers'], df], ignore_index=True)
                        break

            

def get_solution(demands):
    # Create dictionary of actions variable
    actions = [] 

    for i in range(1, 20):                
        currentDemands = demands.loc[demands['time_step'] == i] # Get demands based on time step        

        # Calculate server amount        
        currentDemands.apply(buy, axis=1)     
        print(currentDemands)          

    print(len(dataCentres[0]['servers'].loc[dataCentres[0]['servers']['server_generation'] == 'CPU.S1']) * 60)
    return actions

# BEGIN
for seed in seeds:
    # SET RANDOM SEED
    np.random.seed(seed)

    # GET RANDOMIZED DEMANDS
    actualDemands = get_actual_demand(demandCSV)

    # CALCULATE
    solution = get_solution(actualDemands)