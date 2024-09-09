import pandas as pd
import math

sellingPriceDF = pd.read_csv('data/selling_prices.csv')
serversDF = pd.read_csv('data/servers.csv')
datacentresDF = pd.read_csv('data/datacenters.csv')

def findRevenue(generation, ls, demand):
    sellingPrice = sellingPriceDF.loc[(sellingPriceDF['server_generation'] == generation) & (sellingPriceDF['latency_sensitivity'] == ls)]['selling_price'].values[0].astype(int)
    
    return demand * sellingPrice

def findCost(datacenter, generation, t, expire):
    sI = serversDF.loc[serversDF['server_generation'] == generation]
    dI = datacentresDF.loc[datacentresDF['datacenter_id'] == datacenter]
    
    # Purchase price
    purchasePrice = sI['purchase_price'].values[0].astype(int)

    # Cost of energy consumption
    serverConsumption = sI['energy_consumption'].values[0].astype(int)
    costOfEnergy = dI['cost_of_energy'].values[0].astype(float)
    costOfEC = serverConsumption * costOfEnergy    

    # Server maintenance
    avgFee = sI['average_maintenance_fee'].values[0].astype(int)
    a = (1.5 * t) / expire
    maintenanceCost = avgFee * (1 + a * math.log2(a))

    result = 0
    if t == 1:
        result = purchasePrice + costOfEC + maintenanceCost
    else:
        result = costOfEC + maintenanceCost

    return result

def findProfit(datacenter, generation, ls, t, expire, demand):
    revenue = findRevenue(generation, ls, demand)    
    cost = findCost(datacenter, generation, t, expire)   

    print(revenue, cost)
    return revenue - cost 