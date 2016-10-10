import requests
from .pvdb_exceptions import ApiError
from .pvdb_exceptions import read_api_error
class PvdbRead(object):
    "Read NVDB data"
    
    def __init__(self, client="PVDB", contact="jankyr@vegvesen.no"):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {"X-Client": client,"X-Kontaktperson": contact}
        self.srid = '32633'
        #self.status = self._status()
    
    def _update_params(self, params):
        params.update({'srid':self.srid,'antall':5})
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

    @property
    def catalogue(self):
        return Catalogue(self.baseUrl, self.headers)
            

class Catalogue(object):

    def __init__(self,baseUrl,headers):
        urlAdd = 'vegobjekttyper/?inkluder=alle'
        url = '{baseUrl}/{urlAdd}'.format(baseUrl=baseUrl, urlAdd=urlAdd)
        
        entry = requests.get(url, headers=headers)
        entry = PvdbRead._check_response(entry)

        self._entry = entry
    
    def __len__(self):
        return len(self._entry)

    def __getitem__(self, obj):
        return Entry(self._entry[obj])

class Entry(object):
    def __init__(self, entry):
        self.entry = entry
        self._egenskapstyper = self.entry.pop('egenskapstyper')
        self._relasjonstyper = entry.pop('relasjonstyper')
        self._styringsparametere = entry.pop('styringsparametere')
        self.entry = entry


    @property
    def data(self):
        return self.entry
    
    @property
    def egenskapstyper(self):
        return self._egenskapstyper
    
    @property
    def relasjonstyper(self):
        return self._relasjonstyper
    
    @property
    def styringsparametere(self):
        return self._styringsparametere

