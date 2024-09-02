import pandas as pd

dataCentreCSV = pd.read_csv('data/datacenters.csv')

class DataCentre:    
    def __init__(self, ID):
        self.ID = ID
    

    def getInfo(id, key):
        return dataCentreCSV.loc[dataCentreCSV['datacenter_id'] == id][key]