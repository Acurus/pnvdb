import requests
from .pvdb_exceptions import *
import time

class Nvdb(object):
       
    def __init__(self, client='pvdb', contact='jankyr@vegvesen.no'):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.srid = ''
        self.antall = 10


    @property
    def status(self):
        return _fetch_data(self.baseUrl, 'status')

    
    def objekt(self, objekt_type, nvdb_id):
        return Objekt(objekt_type, nvdb_id)

    
    def objekter(self, objekt_type):
        objekter = []
        return objekter
    

    def objekt_type(self, objekt_type):
        return Objekt_type(objekt_type)
    

    def objekt_typer(self):
        data = _fetch_data(self.baseUrl, 'vegobjekttyper')
        objekt_typer = []
        for objekt_type in data:
            objekt_type_id = objekt_type['id']
            objekt_typer.append(Objekt_type(objekt_type_id, meta=objekt_type))
        return objekt_typer

    def hent(self, objekt_type, payload={}):
        payload.update({'antall':self.antall})
                
        url = '{baseUrl}/vegobjekter/{objekt_type}'.format(baseUrl=self.baseUrl, objekt_type=objekt_type)
        data = requests.get(url, params=payload)
        data = _check_response(data)
        objekter = []
        for obj in data['objekter']:
            objekter.append(Objekt(objekt_type, obj['id']))
        return objekter




class Objekt(Nvdb):
    def __init__(self, objekt_type, nvdb_id):
        super(Objekt, self).__init__()
        self.objekt_type = objekt_type
        self.nvdb_id = nvdb_id
        self.data = None


    @property
    def egengeometri(self):
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter', self.objekt_type, self.nvdb_id)
        if 'geometri' in self.data:
            if self.data['geometri']['egengeometri'] == 'true':
                egengeometri = True
            else:
                egengeometri = False
        return egengeometri

    @property
    def egenskaper(self):
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter', self.objekt_type, self.nvdb_id)
        if 'egenskaper' in self.data:
            egenskaper = self.data['egenskaper']
        else:
            egenskaper = None
        return egenskaper

            
    @property
    def metadata(self):
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter', self.objekt_type, self.nvdb_id)
        if 'metadata' in self.data:
            metadata = self.data['metadata']
        else:
            metadata = None
        return self.data['metadata']


    @property
    def geometri(self):
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter', self.objekt_type, self.nvdb_id)
        if 'geometri' in self.data:
            geometri = self.data['geometri']['wkt']
        else:
            geometri = None
        return geometri


    @property
    def foreldre(self):
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter', self.objekt_type, self.nvdb_id)
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
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter',objekt_type, nvdb_id)
        barn = []
        tid=0
        if 'relasjoner' in self.data and 'barn' in self.data['relasjoner']:
            for i in self.data['relasjoner']['barn']:
                objekt_type = i['type']['id']
                for nvdb_id in i['vegobjekter']:
                    barn.append(Objekt(objekt_type, nvdb_id))
                    end = time.time()
        else:
            barn = None
        return barn

    @property
    def vegreferanser(self):
        if not self.data:
           self.data = _fetch_data(self.baseUrl, 'vegobjekter',objekt_type, nvdb_id)
        vegreferanser = []
        if 'lokasjon' in self.data and 'vegreferanser' in self.data['lokasjon']:
            for i in  self.data['lokasjon']['vegreferanser']:
                vegreferanser.append(i['kortform'])
        else:
            vegreferanser = None
        return vegreferanser


class Objekt_type(Nvdb):
    def __init__(self, objekt_type, meta=None):
        super(Objekt_type, self).__init__()
        self.objekt_type = objekt_type
        self.data = None
        self.meta = meta

       
    @property
    def relasjonstyper(self):
        if not self.data:
            self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
        return self.data['relasjonstyper']

    @property
    def egenskapstyper(self):
        if not self.data:
            self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
        return self.data['egenskapstyper']
    
    @property
    def styringsparametere(self):
        if not self.data:
            self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
        return self.data['styringsparametere']

    @property
    def metadata(self):
        if self.meta:
            return self.meta
        elif not self.data:
            self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
            metadata = self.data.copy()
            del metadata['egenskapstyper']
            del metadata['relasjonstyper']
            del metadata['styringsparametere']
            self.meta = metadata
        return self.meta
    
    
def _fetch_data(baseUrl, url_add, objekt_type=None, nvdb_id=None):
    if nvdb_id:
        url = '{baseUrl}/{url_add}/{objekt_type}/{nvdb_id}'.format(baseUrl=baseUrl,
        url_add=url_add, objekt_type=objekt_type, nvdb_id=nvdb_id)
    elif objekt_type:
        url = '{baseUrl}/{url_add}/{objekt_type}'.format(baseUrl=baseUrl, url_add=url_add, 
        objekt_type=objekt_type)
    else:
        url = '{baseUrl}/{url_add}'.format(baseUrl=baseUrl, url_add=url_add)
    data = requests.get(url)
    data = _check_response(data)
    return data

    
def _check_response(resp):
    '''Function verifes that a 200 code was returned from the API
    and returns the data as Json.
    If a 200 code was not returned, it tries to return the error recived 
    from the API.'''
    
    if resp.status_code == requests.codes.ok:
        return resp.json()
    else:
        print(resp.url)
        raise ApiError(read_api_error(resp))


