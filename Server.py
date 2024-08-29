class Server:
    def __init__(self, ID, generation, Servertype, 
                 capacity, releaseTime, purchasePrice,
                 slotSize, energyConsumption, movingCost, 
                 operatingTime, lifeExp, sellPrice):
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
    
    def __hash__(self, turn, DC) -> str:

       return str(hash(DC,
            turn,
            self.serverGen,
            self.serverType, 
            self.capacity,
            ##Other Parameters
            ))

    
    def __eq__(self, other)

        return self.serverID == other.serverID 