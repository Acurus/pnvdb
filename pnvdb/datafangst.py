from . import config
from pnvdb.var import auth
import requests
import geojson
import json

class Datafangst(object):
    def __init__(self, username=None, password=None, contractId=None):
        self.base_url = config.datafangst_base_url
        self.headers = {
                    'Content-Type': "application/geo+json",
                    'Accept': "application/json"
                  }
        self.url = "{baseurl}/{contractId}/featurecollection".format(baseurl=self.base_url, contractId=contractId)
        
    def feature_collection(self):
        return FeatureCollection(self.url, self.headers)

    def feature(self, objekt_type, coordinates, tag):
        return Feature(objekt_type, coordinates, tag)

class FeatureCollection(object):
    ''' Class for defining a set of objects ready to push to datafangst'''
    def __init__(self, url, headers):
        self.features = []
        self.status_src = None
        self.url = url
        self.headers = headers
    
    def add_feature(self, feature):
        #self.features.append(feature.__repr__())
        self.features.append(feature)
    
    def push(self):
        feature_collection = geojson.FeatureCollection(self.features)
        response = requests.post(self.url, data=geojson.dumps(feature_collection).encode('utf8'),
                                 headers=self.headers,auth=(auth.username, auth.password))
        self.status_src = json.loads(response.text)['resources'][1]['src']
        return self.status()
        
    def status(self):
        if self.status:
            return requests.get(self.status_src, auth=(auth.username, auth.password)).text
        else:
            return None

        
class Feature(object):
    '''Class for defining objects ready to push to Datafangst'''
    def __init__(self, objekt_type, coordinates, tag):
        self._objekt_type = objekt_type
        self._coordinates = None
        self.properties = {}
        self.coordinates(coordinates)
        self.properties["typeId"] = objekt_type
        self.properties["tag"] = tag
        self.properties["dataCatalogVersion"] = "2.13"

    def coordinates(self, geometry):
        if isinstance(geometry, list):
            if geometry[0] == geometry[-1]:
                self._coordinates = geojson.Polygon([geometry])
            else:
                self._coordinates = geojson.LineString(geometry)
        else:
            self._coordinates = geojson.Point(geometry)

    def attribute(self, attribute_id, attribute_value):
        self.properties['attributes'] = {str(attribute_id):attribute_value}

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
        


    
