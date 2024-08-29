class DataCentre : 
    ##Class Objects for DataCentre 
    def __Init__(self, dataCentreID):
        self.dataCentreID = dataCentreID 
        self.allActions = {}
        self.timeStep = 1
        self.Servers = {}
        pass 

    
    def setEnergyCost(self, cost) -> None:
        self.energyCost = cost
        return 
    

    def setLatency(self, latency) -> None:
        self.latency = latency 
        return
    

    def setCapacity(self, capacity) -> None:
        self.capacity = capacity
        return 

    def setAction(self, action) -> None:
        ##Moves old actions into a dictionary 
        ##With key representing the turn it was made in 
        ##and replaces the currentAction with the latest action of the data centre 
        if (self.currentAction is not None):
            self.allActions[self.timeStep] = self.currentAction
        self.currentAction = action 
        return
       

    def buyServer(self, serverData, serverID) -> None:
        self.Servers[serverID] = serverData
        print("Server has been obtained")
        return 
    

    def moveServer(self, serverID) -> object:
        serverObject = self.Servers[serverID]
        del self.Servers[serverID]
        return serverObject


    def nextTurn(self) -> None:
        self.timeStep += 1 
        return
