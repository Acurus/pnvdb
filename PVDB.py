import requests

class PVDBread:
    "Read NVDB data"
    
    def __init__(self):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2/'
        self.headers = {'user-agent': 'kyrdalen.no'}
    
    def checkResponse(self, resp):
        if True:
            return resp

    def getRoadObjects(self):
        url = self.baseUrl
        data = requests.get(self.baseUrl,headers=self.headers)
        return self.checkResponse(data.json())

    def getRoadObjectTypes():
        pass
    def getRoadLinks():
        pass
    def getAreas():
        pass
    def getPosition():
        pass
    def GetRoad():
        pass
    def GetStatus():
        pass
