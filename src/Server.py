import pandas as pd

serverCSV = pd.read_csv('data/servers.csv')

def getInfo(g, key):
    return serverCSV.loc[serverCSV['server_generation'] == g][key]