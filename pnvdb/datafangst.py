from . import config
import requests
import geojson
"""
{
"type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [ [10.39241731, 63.43053048],
            [10.39495434, 63.43043698],
            [10.39579151, 63.42898665],
            [10.39272171, 63.42909269],
            [10.39241731, 63.43053048] ]
        ]
      },
      "properties": {
        "tag": "Forsterkningslag#1",
        "dataCatalogVersion": "2.06",
        "typeId": 227,
        "comment": "Usikker på måledatoen",
        "attributes": {
          "5543": "20160802"
         }
       }
    }
  ]
}

"""
class Datafangst(object):
    def __init__(self, username=None, password=None, contractId=None):
        self.base_url = config.datafangst_base_url
        #self.headers = {'X-OpenAM-Username': username,
        #  'X-OpenAM-Password': password, 
        #  'Content-Type': 'application/geojson'}
        self.headers = {'Content-Type': 'application/geojson'}
        
        
        url = '{base_url}/api/v1/contract/{contractId}'.format(base_url=self.base_url, contractId=contractId)
        #res = requests.get(url, headers=self.headers, auth=(username, password))
        

class FeatureCollection(object):
    ''' Class for defining a set of objects ready to push to datafangst'''
    def __init__(self):
        self.features = []
    
    def add_feature(self, feature):
        #self.features.append(feature.__repr__())
        self.features.append(feature)
    
    def push(self):
        feature_collection = geojson.FeatureCollection(self.features)
        return feature_collection

class Feature(object):
    '''Class for defining objects ready to push to Datafangst'''
    def __init__(self, objekt_type, coordinates, tag):
        self._objekt_type = objekt_type
        self._coordinates = None
        self.properties = {}
        self.coordinates(coordinates)
        self.properties["typeId"] = objekt_type
        self.properties["tag"] = tag

    def coordinates(self, geometry):
        self._coordinates = geojson.Polygon(geometry)

    def attribute(self, attribute_id, attribute_value):
        self.properties[str(attribute_id)] = attribute_value

    def comment(self, comment):
        self.properties["comment"] = comment
    
    def tag(self, tag):
        self.properties["tag"] = tag
    
    def __repr__(self):
        feature = geojson.Feature(geometry=self._coordinates,
                                  properties=self.properties)
        return geojson.dumps(feature)
    
    def feature(self):
        return geojson.Feature(geometry=self._coordinates,
                                  properties=self.properties)
        


    