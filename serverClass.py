class Server:
    def __init__(self, ID, generation, Servertype, 
                 capacity, releaseTime, purchasePrice,
                 slotSize, energyConsumption, movingCost, 
                 operatingTime, lifeExp, sellPrice) -> None:
        self.ID = ID
        self.generation = generation
        self.type = Servertype
        self.capacity =  capacity
        self.releaseTime = releaseTime
        self.purchasePrice = purchasePrice
        self.slotSize = slotSize
        self.energyConsumption = energyConsumption
        self.movingCost = movingCost
        self.operatingTime = operatingTime
        self.lifeExp = lifeExp
        self.sellPrice = sellPrice
        pass

    
    def __eq__(self, other) -> bool: 

        return self.serverID == other.serverID 


##To generate a unique ID for the server class.
def generateUniqueID(serverType, timeStep, DC):
    ID = hash((serverType, timeStep, DC ))
    return ID 