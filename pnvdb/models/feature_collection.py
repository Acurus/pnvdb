import json

import geojson
import requests


class FeatureCollection(object):
    ''' Class for defining a set of objects ready to push to datafangst'''

    def __init__(self, url, username, password, headers):
        self.username = username
        self.password = password
        self.features = []
        self.status_src = None
        self.url = url
        self.headers = headers

    def add_feature(self, feature):
        """ Method that adds a `.Feature` to the instance"""
        self.features.append(geojson.Feature(geometry=feature._coordinates,
                                             properties=feature.properties))

    def push(self):
        """ Method that pushes the FeatureCollection to datafangst
            
            :returns: xml respons from datafangst
        """
        feature_collection = geojson.FeatureCollection(self.features)
        response = requests.post(self.url, data=geojson.dumps(feature_collection).encode('utf8'),
                                 headers=self.headers, auth=(self.username, self.password))

        if response.status_code == 202:
            self.status_src = json.loads(response.text)['resources'][1]['src']
            return self.status()
        else:
            response.raise_for_status()

    def status(self):
        """ Method for polling the status of the instance from datafangst
            returns None if data not pushed to datafangst
            
            :returns: xml respons from datafangst
        """
        if self.status_src:
            return requests.get(self.status_src, auth=(self.username, self.password)).text
        else:
            return 'Not pushed'
    
    def __repr__(self):
        return self.status

