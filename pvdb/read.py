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

    def objekt(self, objekt_type, nvdb_id):
        return Objekt(objekt_type, nvdb_id)


class Objekt(Nvdb):
    def __init__(self, objekt_type, nvdb_id):
        super(Objekt, self).__init__()
        self.objekt_type = objekt_type
        self.nvdb_id = nvdb_id
        self.fetched = False

    @property
    def egengeometri(self):
        if not self.fetched:
            self._fetch_data()
        if 'geometri' in self.data:
            if self.data['geometri']['egengeometri'] == 'true':
                egengeometri = True
            else:
                egengeometri = False
        return egengeometri

    @property
    def egenskaper(self):
        if not self.fetched:
            self._fetch_data()
        if 'egenskaper' in self.data:
            egenskaper = self.data['egenskaper']
        else:
            egenskaper = None
        return egenskaper

            
    @property
    def metadata(self):
        if not self.fetched:
            self._fetch_data()
        if 'metadata' in self.data:
            metadata = self.data['metadata']
        else:
            metadata = None
        return self.data['metadata']


    @property
    def geometri(self):
        if not self.fetched:
            self._fetch_data()
        if 'geometri' in self.data:
            geometri = self.data['geometri']['wkt']
        else:
            geometri = None
        return geometri


    @property
    def foreldre(self):
        if not self.fetched:
            self._fetch_data()
        foreldre = []
        if 'relasjoner' in self.data and 'foreldre' in self.data['relasjoner']:
            for i in self.data['relasjoner']['foreldre']:
                objekt_type = i['type']['id']
                for nvdb_id in i['vegobjekter']:
                    foreldre.append(Objekt(objekt_type, nvdb_id))
        else:
            foreldre = None
        return foreldre

    @property
    def barn(self):
        if not self.fetched:
            self._fetch_data()
        barn = []
        if 'relasjoner' in self.data and 'barn' in self.data['relasjoner']:
            for i in self.data['relasjoner']['barn']:
                objekt_type = i['type']['id']
                for nvdb_id in i['vegobjekter']:
                    barn.append(Objekt(objekt_type, nvdb_id))
        else:
            barn = None
        return barn

    @property
    def vegreferanser(self):
        if not self.fetched:
            self._fetch_data()
        vegreferanser = []
        if 'lokasjon' in self.data and 'vegreferanser' in self.data['lokasjon']:
            for i in  self.data['lokasjon']['vegreferanser']:
                vegreferanser.append(i['kortform'])
        else:
            vegreferanser = None
        return vegreferanser

    def _fetch_data(self):
        args = {}
        params = _update_params(args)
        url = '{baseUrl}/vegobjekter/{objekt_type}/{nvdb_id}'.format(baseUrl=self.baseUrl,
            objekt_type=self.objekt_type, nvdb_id=self.nvdb_id, params = params)
        data = requests.get(url)
        self.data = _check_response(data)
        self.fetched = True


class objekt_type(Nvdb):
    def __init__(objekt_type):
        super(objekt_type, self).__init__()
        self.objekt_type = objekt_type
        

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


