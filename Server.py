import pandas as pd

serverCSV = pd.read_csv('data/servers.csv')

class Server:
    def __init__(self, ID, generation, boughtTimeStep):
        self.ID = ID
        self.generation = generation
        self.boughtTimeStep = boughtTimeStep        
    
    def getInfo(g, key):
        return serverCSV.loc[serverCSV['server_generation'] == g][key]