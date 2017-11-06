import requests
from .pnvdb_exceptions import *
class NVDBase(object):
    """Superclass for all models in pvdb"""
    def __init__(self, client, contact):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.srid = ''
        self.antall = 1000



def _fetch_data(nvdb, url_add, payload={}, format='json'):
    url = '{baseUrl}/{url_add}'.format(baseUrl=nvdb.baseUrl, url_add=url_add)
    resp = requests.get(url, params=payload, headers=nvdb.headers)
    #print(resp.headers)
    #print(resp.url)
    data = _check_response(nvdb, resp, format)
    return data

def _check_response(nvdb, resp, format='json'):
    """Function verifes that a 200 code was returned from the API
    and returns the data as Json.
    If a 200 code was not returned, it tries to return the error recived 
    from the API."""
    if resp.status_code == requests.codes.ok and format == 'json':
        return resp.json()
    elif resp.status_code == requests.codes.ok and format == 'xml':
        return resp
    else:
        print(resp.url)
        raise ApiError(read_api_error(resp))