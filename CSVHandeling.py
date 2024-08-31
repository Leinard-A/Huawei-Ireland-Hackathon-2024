import csv
import os
import json

class FileHandling:
    def __init__(self, fileName):
        self.fileName = fileName
        self.fileData = None

    def checkFileExists(self):
        # Check if the file exists
        if not os.path.isfile(self.fileName):
            raise FileNotFoundError(f"The file {self.fileName} does not exist.")
        return True

    def accessFileData(self):
        # Check if the file exists before accessing it
        if self.checkFileExists():
            with open(self.fileName, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.fileData = [row for row in reader]
        return self.fileData

    def convertToJson(self):
        # Convert CSV file to JSON
        if self.fileData is None:
            self.accessFileData()
        return json.dumps(self.fileData, indent=4)

# test ./data/servers.csv
fileHandler = FileHandling('./data/servers.csv')
try:
    jsonData = fileHandler.convertToJson()
    print(jsonData)
except FileNotFoundError as outpute:
    print(outpute)
