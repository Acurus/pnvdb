from . import config
import requests

class Datafangst(object):
    def __init__(self, username=None, password=None, contractId=None):
        self.base_url = config.datafangst_base_url
        self.headers = {'X-OpenAM-Username': username,
          'X-OpenAM-Password': password, 
          'Content-Type': 'application/geojson'}
        
        
        url = '{base_url}/api/v1/contract/{contractId}'.format(base_url=self.base_url, contractId=contractId)
        res = requests.get(url, headers=self.headers)#, auth=(username, password))
        print('Get Contract status: {}'.format(res.status_code))
        print(res.content)
        



        
        
