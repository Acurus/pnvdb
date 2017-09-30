# -*- coding: utf-8 -*-
import requests
from .pvdb_exceptions import *
import time

class Nvdb(object):
       
    def __init__(self, client='pvdb', contact='jankyr@vegvesen.no'):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.srid = ''
        self.antall = 1000


    def status(self):
        return _fetch_data(self.baseUrl, 'status')

    
    def objekt(self, objekt_type, nvdb_id):
        return Objekt(objekt_type, nvdb_id)


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
        neste = '{baseUrl}/vegobjekter/{objekt_type}'.format(baseUrl=self.baseUrl, objekt_type=objekt_type)
        data = _check_response(requests.get(neste, params=payload))
        while True:
            metadata = data['metadata']
            returnert = metadata['returnert']
            if returnert == 0:
                break
            neste = metadata['neste']['href']
            for obj in enumerate(data['objekter']):
                yield Objekt(objekt_type, obj[1]['id'])
            data = _check_response(requests.get(neste))
        


    def omrader(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/{}'.format(area_type)
        payload = {'inkluder':'alle'}
        return _check_response(requests.get(url, params=payload))
    
    def regioner(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/regioner'
        payload = {'inkluder':'alle'}
        data = _check_response(requests.get(url, params=payload))
        return [Area(area_data) for area_data in data]

    def fylker(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/fylker'
        payload = {'inkluder':'alle'}
        data = _check_response(requests.get(url, params=payload))
        return [Area(area_data) for area_data in data]

    def vegavdelinger(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/vegavdelinger'
        payload = {'inkluder':'alle'}
        data = _check_response(requests.get(url, params=payload))
        return [Area(area_data) for area_data in data]

    def kommuner(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/kommuner'
        payload = {'inkluder':'alle'}
        data = _check_response(requests.get(url, params=payload))
        return [Area(area_data) for area_data in data]

    def kontraktsomrader(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/kontraktsomrader'
        payload = {'inkluder':'alle'}
        data = _check_response(requests.get(url, params=payload))
        return [Area(area_data) for area_data in data]

    def riksvegruter(self):
        url = 'https://www.vegvesen.no/nvdb/api/v2/omrader/riksvegruter'
        payload = {'inkluder':'alle'}
        data = _check_response(requests.get(url, params=payload))
        return [Area(area_data) for area_data in data]

    def posision(self):
        pass

    def veg(self):
        pass


class Area(Nvdb):
    def __init__(self, area_data):
        super(Area, self).__init__()
        self.data = area_data

    @property
    def metadata(self):
        metadata = self.data.copy()
        if 'kartutsnitt' in self.data:
            del metadata['kartutsnitt']
        if 'senterpunkt' in self.data:
            del metadata['senterpunkt']
        if 'vegobjekt' in self.data:
            del metadata['vegobjekt']
        return metadata


    @property
    def kartutsnitt(self):
        if 'kartutsnitt' in self.data:
            return self.data['kartutsnitt']
        else:
            return None
    
    
    @property
    def senterpunkt(self):
        if 'senterpunkt' in self.data:
            return self.data['senterpunkt']
        else:
            return None
    

    @property
    def objekt(self):
        objekttype = self.data['vegobjekt']['type']
        nvdb_id = self.data['vegobjekt']['id']
        return Objekt(objekttype, nvdb_id)

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

    def dump(self, format='json'):
        if format.lower() == 'json':
            if not self.data:
                self.data = _fetch_data(self.baseUrl, 'vegobjekter', self.objekt_type)
            return self.data
        
        elif format.lower() == 'xml':
            url = '{baseUrl}/vegobjekter/{objekt_type}/{nvdb_id}.xml'.format(baseUrl=self.baseUrl,
                objekt_type=self.objekt_type, nvdb_id=self.nvdb_id)
            resp = requests.get(url)
            print(resp.url)
            if resp.status_code == requests.codes.ok:
                xml_data = resp.text
            else:
                raise ApiError(read_api_error(resp))
            return xml_data

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

    def dump(self, format='json'):
        if format.lower() == 'json':
            if not self.data:
                self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
            return self.data
        
        elif format.lower() == 'xml':
            url = '{baseUrl}/vegobjekttyper/{objekt_type}.xml'.format(baseUrl=self.baseUrl, 
                objekt_type=self.objekt_type)
            resp = requests.get(url)
            print(resp.url)
            if resp.status_code == requests.codes.ok:
                xml_data = resp.text
            else:
                raise ApiError(read_api_error(resp))
            return xml_data

            
       
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

    @property
    def barn(self):
        if not self.data:
            self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
        realasjoner = self.data['relasjonstyper']
        return [Objekt_type(i['type']['id']) for i in realasjoner['barn']]
    @property
    def foreldre(self):
        if not self.data:
            self.data = _fetch_data(self.baseUrl, 'vegobjekttyper', self.objekt_type)
        realasjoner = self.data['relasjonstyper']
        return [Objekt_type(i['type']['id']) for i in realasjoner['foreldre']]
                
    
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