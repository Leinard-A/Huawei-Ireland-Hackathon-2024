class Server:
    def __init__(self, ID, generation, type, 
                 capacity, releaseTime, purchasePrice,
                 slotSize, energyConsumption, movingCost, 
                 operatingTime, lifeExp, sellPrice):
        self.ID = ID
        self.generation = generation
        self.type = type
        self.capacity =  capacity
        self.releaseTime = releaseTime
        self.purchasePrice = purchasePrice
        self.slotSize = slotSize
        self.energyConsumption = energyConsumption
        self.movingCost = movingCost
        self.operatingTime = operatingTime
        self.lifeExp = lifeExp
        self.sellPrice = sellPrice