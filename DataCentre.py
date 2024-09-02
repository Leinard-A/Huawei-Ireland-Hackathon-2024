import pandas as pd

dataCentreCSV = pd.read_csv('data/datacenters.csv')

def createDataCentres(size):
    dcDicts = []
    for i in range(1, size + 1):
        ID = 'DC' + str(i)
        df = pd.DataFrame(columns=['server_id', 'server_generation', 'slot_size', 'bought_date','expire_date'])

        dcDict = {
            'id': ID,
            'servers': df,
            'latency_sensitivity': DataCentre.getInfo(ID, 'latency_sensitivity').values,
            'slots_capacity': DataCentre.getInfo(ID, 'slots_capacity').values[0].astype(int)
        }

        dcDicts.append(dcDict)
    
    return dcDicts


class DataCentre:    
    def __init__(self, ID):
        self.ID = ID
    

    def getInfo(id, key):
        return dataCentreCSV.loc[dataCentreCSV['datacenter_id'] == id][key]