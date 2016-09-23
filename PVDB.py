import requests

class PvdbRead:
    "Read NVDB data"
    
    def __init__(self):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {"X-Client": "PVDB","X-Kontaktperson": "jankyr@vegvesen.no"}
        self.segmentation = 'true'
        self.srid = '32633'
        
    
    def check_response(self, resp):
        if True:
            return resp

    def get_road_objects(self, obj, params):
        self.paramUpdate = {'segmentering':self.segmentation,'srid':self.srid}
        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}'.format(baseUrl=self.baseUrl, urlAdd=urlAdd, obj=obj)
        params.update(self.paramUpdate)
        print(params)
        data = requests.get(url, params = params, headers=self.headers).json()
        return self.checkResponse(data)
    
    def get_road_object(self, obj, objectID):
        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}/{objectID}'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, obj=obj, objectID=objectID)
        data = requests.get(url).json()
        return self.checkResponse(data)


    def get_road_objectTypes():
        pass
    def get_road_links():
        pass
    def get_areas():
        pass
    def get_position():
        pass
    def Get_road():
        pass
    def Get_status():
        pass

class PvdbWrite:
        def __init__(self):
            pass