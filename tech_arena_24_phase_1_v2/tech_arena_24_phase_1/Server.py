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
        self.purchePrice = purchasePrice
        self.slotSize = slotSize
        self.energyConsumption = energyConsumption
        self.movingCost = movingCost
        self.operatingTime = operatingTime
        self.lifeExp = lifeExp
        self.sellPrice = sellPrice
    
    def getID(self):
        print(self.serverID)


newS = server(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
newS.getID()