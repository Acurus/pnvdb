import requests
from .core import *

class Catalogue(object):
    def __init__(self, client='PVDB', contact='jankyr@vegvesen.no'):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.urlAdd = 'vegobjekttyper'
                
    def objects(self, params):
        url = '{baseUrl}/{urlAdd}'.format(baseUrl=self.baseUrl, urlAdd=self.urlAdd)
        resp = requests.get(url, params=params, headers=self.headers)
        return check_response(resp)
    
    def object(self, objcode, params):
        url = '{baseUrl}/{urlAdd}/{objcode}'.format(
                baseUrl=self.baseUrl, urlAdd=self.urlAdd, objcode=objcode)
        resp = requests.get(url, params=params, headers=self.headers)
        return check_response(resp)    
