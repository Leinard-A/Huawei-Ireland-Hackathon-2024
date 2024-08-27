class Server:
    ##Class Objects for the potential Server
    
    ##Going to need to cache the names of serverIDs to be able to prevent the checking of earlier serverIDs being too long.

    def __Init__(self, serverID, 
                 serverGen, serverType, capacity) -> None:
        self.serverID = serverID## We could make this the hash value of the collection of data in a way to prevent duplications.
        self.serverGen = serverGen
        self.serverType = serverType
        self.capacity = capacity 
        ##Self Explanatory
        pass 

class DataCentre : 
    ##Class Objects for DataCentre 
    def __Init__(self, dataCentreID):
        self.dataCentreID = dataCentreID 
        self.allActions = {}
        self.timeStep = 1
        self.Servers = {}
        self.potentialActions = [
        'buy',##Buy a Serve r
        'move',##Move it to a new Data Location 
        'hold',## Not do anything 
        'dismiss'##Shut down Server 
        ]
        pass 
    
    def setAction(self, action) -> None:
        ##Moves old actions into a dictionary 
        ## With key representing the turn it was made in 

        ## and replaces the currentAction with the latest action of the data centre 
        self.allActions[self.timeStep] = self.currentAction
        self.currentAction = action 
        return

    def getAction(self) -> str:
        return self.currentActions
    
    def moveServer(self, serverID) -> object:
        serverObject = self.Servers[serverID]
        del self.Servers[serverID]
        return serverObject
    
    def getServer(self, serverData, serverID) -> None:
        self.Servers[serverID] = serverData
        print("Server has been obtained")
        return



class fileHandeling:

    def __Init__(self, fileName):
        self.fileName = fileName
        pass 

    def checkFileExists(self):
        ##Check File exists 
        ## Otherwise chuck error message 
        pass 

    def accessFileData(self):
        ##Access file data and save data to be stored in a dict
        
        ##self.fileData = fileData
        pass 
