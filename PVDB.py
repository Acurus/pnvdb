import requests

class PVDBread:
    "Read NVDB data"
    
    def __init__(self):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {"X-Client": "PVDB","X-Kontaktperson": "jankyr@vegvesen.no"}
        self.segmentation = 'true'
        self.srid = '32633'
        
    
    def checkResponse(self, resp):
        if True:
            return resp

    def getRoadObjects(self,obj,params):
        self.paramUpdate = {'segmentering':self.segmentation,'srid':self.srid}
        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}'.format(baseUrl=self.baseUrl,urlAdd=urlAdd,obj=obj)
        params.update(self.paramUpdate)
        print(params)
        data = requests.get(url, params = params, headers=self.headers).json()
        return self.checkResponse(data)
    
    def getRoadObject(self,obj,objectID):
        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}/{objectID}'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd,obj=obj,objectID=objectID)
        data = requests.get(url).json()
        return self.checkResponse(data)


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
