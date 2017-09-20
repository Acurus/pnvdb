import requests
from .pvdb_exceptions import *


class Nvdb(object):
       
    def __init__(self, client='PVDB', contact='jankyr@vegvesen.no'):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.srid = ''


    @property
    def status(self):
        status = requests.get('https://www.vegvesen.no/nvdb/api/v2/status')
        return _check_response(status)

    def object(self, object_type, nvdb_id):
        return Object(object_type, nvdb_id)


class Object(Nvdb):
    def __init__(self, object_type, nvdb_id):
        super(Object, self).__init__()
        self.object_type = object_type
        self.nvdb_id = nvdb_id
        self.fetched = False


    @property
    def attributes(self):
        if not self.fetched:
            self._fetch_data()
        return self.data['egenskaper']

            
    @property
    def metadata(self):
        if not self.fetched:
            self._fetch_data()
        return self.data['metadata']


    @property
    def geometry(self):
        if not self.fetched:
            self._fetch_data()
        return self.data['geometri']


    @property
    def relations(self):
        if not self.fetched:
            self._fetch_data()
        return self.data['relasjoner']


    def _fetch_data(self):
        args = {}
        params = _update_params(args)
        url = '{baseUrl}/vegobjekter/{object_type}/{nvdb_id}'.format(baseUrl=self.baseUrl,
            object_type=self.object_type, nvdb_id=self.nvdb_id, params = params)
        data = requests.get(url)
        self.data = _check_response(data)
        self.fetched = True


class Object_type(Nvdb):
    def __init__(Object_type):
        super(Object_type, self).__init__()
        self.object_type = object_type
        

def _update_params(params):
    params.update({'antall':5})
    return params

    
def _check_response(resp):
    '''Function verifes that a 200 code was returned from the API
    and returns the data as Json.
    If a 200 code was not returned, it tries to return the error recived 
    from the API.'''
    
    if resp.status_code == requests.codes.ok:
        return resp.json()
    else:
        raise ApiError(read_api_error(resp))


