import pandas as pd

dataCentreCSV = pd.read_csv('data/datacenters.csv')


def getInfo(id, key):
    return dataCentreCSV.loc[dataCentreCSV['datacenter_id'] == id][key]

def createDataCentres():
    # Each data centre is a dictionary
    dcDicts = []
    for i in range(1, 5):
        ID = 'DC' + str(i)
        df = pd.DataFrame(columns=['server_id', 'server_generation', 'slot_size', 'buy_date','expire_date'])

        # Creating data centres
        dcDict = {
            'ID': ID,
            'servers': df,
            'latency_sensitivity': getInfo(ID, 'latency_sensitivity').values,
            'slots_capacity': getInfo(ID, 'slots_capacity').values[0].astype(int)
        }

        dcDicts.append(dcDict)
    
    return dcDicts