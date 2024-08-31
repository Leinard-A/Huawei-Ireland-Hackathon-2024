import pandas as pd

serverCSV = pd.read_csv('data/servers.csv')

class Server:
    def __init__(self, ID, generation):
        self.ID = ID
        self.generation = generation

        info = serverCSV[serverCSV['server_generation'] == generation]
        self.purchase = info['purchase_price'].values.astype(int)
        self.slotsSize = info['slots_size'].values.astype(int)
        self.energyConsumption = info['energy_consumption'].values.astype(int)
        self.capacity = info['capacity'].values.astype(int)
        self.lifeExp = info['life_expectancy'].values.astype(int)
        self.movingCost = info['cost_of_moving'].values.astype(int)
        self.avgMaintenance = info['average_maintenance_fee'].values.astype(int)