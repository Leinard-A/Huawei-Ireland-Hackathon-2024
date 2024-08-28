class server(object):
    def __init__(self, serverID, serverGen, serverType, 
                 capacity, releaseTime, purchasePrice,
                 slotSize, energyConsumption, movingCost, 
                 operatingTime, lifeExp, sellPrice):
        self.serverID = serverID
        self.serverGen = serverGen
        self.serverType = serverType
        self.capacity =  capacity
        self.releaseTime = releaseTime
        self.purchasePrice = purchasePrice
        self.slotSize = slotSize
        self.energyConsumption = energyConsumption
        self.movingCost = movingCost
        self.operatingTime = operatingTime
        self.lifeExp = lifeExp
        self.sellPrice = sellPrice
    
    def getID(self):
        return self.serverID
    
    def getGen(self):
        return self.serverGen
    
    def getType(self):
        return self.serverType
    
    def getCapacity(self):
        return self.capacity
    
    def getReleaseTime(self):
        return self.releaseTime

    def getPurchasePrice(self):
        return self.purchasePrice
    
    def getSlotSize(self):
        return self.slotSize
    
    def getEnergyConsumption(self):
        return self.energyConsumption
    
    def getMovingCost(self):
        return self.movingCost

    def getOperatingTime(self):
        return self.operatingTime
    
    def getLifeExp(self):
        return self.lifeExp

    def getSellPrice(self):
        return self.sellPrice