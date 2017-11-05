# -*- coding: utf-8 -*-
import requests
from .pnvdb_exceptions import *

class Nvdb(object):
    """ The main class for interfacing with the API.
        
        :param client: Name of client using the API
        :type name: str
        :param contact: Contact information of user of the API
        :returns:  Nvdb Class

        >>> import pnvdb
        >>> nvdb = pnvdb.Nvdb(client='Your-App-Name', contact='Your-contact-information')

        
    """
       
    def __init__(self, client='pnvdb', contact=''):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.srid = ''
        self.antall = 1000

    def _fetch_data(self, url_add, payload={}, format='json'):
        url = '{baseUrl}/{url_add}'.format(baseUrl=self.baseUrl, url_add=url_add)
        resp = requests.get(url, params=payload, headers=self.headers)
        #print(resp.headers)
        #print(resp.url)
        data = self._check_response(resp, format)
        return data

    def _check_response(self, resp, format='json'):
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

    def status(self):
        """ Method for getting information about the current status of the API 
            
            >>> status = nvdb.status()
            >>> print(status['datakatalog']['versjon'])
            2.10

            :returns: Dict
        """
        return self._fetch_data('status')
    
    def objekt(self, objekt_type, nvdb_id):
        """ Method for creating a spesific nvdb python Objekt

            :param objekt_type: nvdb objekttype id.
            :type name: int
            :param nvdb_id: the unique nvdb id
            :type name: int
            :returns: :class:`.Objekt`

            >>> obj = nvdb.objekt(objekt_type=67, nvdb_id=89204552)
            >>> print(obj.metadata)
            {'versjon': 3, 'type': {'navn': 'Tunnelløp', 'id': 67}, 'startdato': '2014-01-17', 'sist_modifisert': '2017-10-23 15:15:50'}

        """
        return Objekt(objekt_type, nvdb_id)


    def objekt_type(self, objekt_type):
        """ Method for creating a spesific nvdb python

            :param objekt_type: nvdb objekttype id.
            :type name: int
            :returns: :class:`.Objekt_type`

            >>> obj = nvdb.objekt_type(objekt_type=67)
            >>> print(obj.metadata['sosinvdbnavn'])
            Tunnelløp_67
        """
        return Objekt_type(objekt_type)
    

    def objekt_typer(self):
        """ Returns objekt_type of every avaliable obj type in nvdb
            
            :returns: List of :class:`.Objekt_type`
            
            >>> obj_types = nvdb.objekt_typer()
            >>> print(obj_types[0].metadata['sosinvdbnavn'])
            Skjerm_3

        """
        data = self._fetch_data('vegobjekttyper')
        objekt_typer = []
        for objekt_type in data:
            objekt_type_id = objekt_type['id']
            objekt_typer.append(Objekt_type(objekt_type_id, meta=objekt_type))
        return objekt_typer


    def hent(self, objekt_type, payload={}):
        """ Return a generator object that can be itterated over
            to fetch the results of the query.
            
            :param objekt_type: nvdb objekttype id.
            :type payload: dict
            :returns: generator of :class:`.Objekt`
            
            >>> criteria = {'fylke':'2','egenskap':'1820>=20'}
            >>> bomstasjoner = nvdb.hent(45, criteria)
            >>> for bomstasjon in bomstasjoner:
            >>>     print(bomstasjon)
        """
        payload.update({'antall':self.antall})
        url = 'vegobjekter/{objekt_type}'.format(objekt_type=objekt_type)
        data = self._fetch_data(url, payload=payload)
        while True:
            metadata = data['metadata']
            returnert = metadata['returnert']
            if returnert == 0:
                break
            
            payload.update({'start':metadata['neste']['start']})
            for obj in enumerate(data['objekter']):
                yield Objekt(objekt_type, obj[1]['id'])
            data = self._fetch_data(url, payload)
        
    def vegreferanse(self, vegreferanse):
        """ Return vegreferanse object.
            PS : Only support point refferences

            :param vegreferanse: The road refferences to objectify
            :type vegreferanse: string
            :returns: :class:`.Vegreferanse`

            >>> print(nvdb.vegreferanse('1600Ev6hp12m1000'))
        """
        if type(vegreferanse) == list:
            payload = {'vegreferanser':','.join(vegreferanse)}
            result = self._fetch_data('veg/batch', payload)
            return [Vegreferanse(vegref, meta=result[vegref]) for vegref in vegreferanse]
        return Vegreferanse(vegreferanse)
    

    def posisjon(self, x=None, y=None, lat=None, lon=None):
        """Returns a posisjon object for a given location
            
            :param x: X-coordinate in EUREF89 UTM 33
            :type x: float
            :param y: Y-coordinate in EUREF89 UTM 33
            :type y: float
            :param lat: Lattitude in EUREF89
            :type lat: float
            :param lon: Longitude in EUREF89
            :type lon: float
            :returns: :class:`.Posisjon`

            >>> pos = nvdb.posisjon(x=269815,y=7038165)
            >>> print(pos.vegreferanse)
        """
        if x and y:
            payload = {'nord':y,'ost':x}
        elif lat and lon:
            payload = {'lat':lat,'lon':lon}

        return Posisjon(payload)
    
   
    def regioner(self):
        """ Returns an Area object for all regions
            
            :returns: list of :class:`.Area`

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = self._fetch_data('omrader/regioner', payload)
        return [Area(area_data) for area_data in data]

    def fylker(self):
        """ Returns an Area object for all fylker

            :returns: list of :class:`.Area`

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = self._fetch_data('omrader/fylker', payload)
        return [Area(area_data) for area_data in data]

    def vegavdelinger(self):
        """ Returns an Area object for all vegavdelinger

            :returns: list of :class:`.Area`

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = self._fetch_data('omrader/vegavdelinger', payload)
        return [Area(area_data) for area_data in data]

    def kommuner(self):
        """ Returns an Area object for all kommuner

            :returns: list of :class:`.Area`

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = self._fetch_data('omrader/kommuner', payload)
        return [Area(area_data) for area_data in data]

    def kontraktsomrader(self):
        """ Returns an Area object for all kontraktsomrader

            :returns: list of :class:`.Area`

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = self._fetch_data('omrader/kontraktsomrader', payload)
        return [Area(area_data) for area_data in data]

    def riksvegruter(self):
        """ Returns an Area object for all riksvegruter

            :returns: list of :class:`.Area`

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = self._fetch_data('omrader/riksvegruter', payload)
        return [Area(area_data) for area_data in data]

class Area(Nvdb):
    """ Class for area objects. """ 
    def __init__(self, area_data):
        super(Area, self).__init__()
        self.data = area_data

    @property
    def metadata(self):
        """ 
        :Attribute: Dict
        """
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
        """ 
        :Attribute: Well Known Text
        """
        if 'kartutsnitt' in self.data:
            return self.data['kartutsnitt']['wkt']
        else:
            return None
    
    
    @property
    def senterpunkt(self):
        """
        :Attribute: Well Known Text
        """
        if 'senterpunkt' in self.data:
            return self.data['senterpunkt']['wkt']
        else:
            return None
    

    @property
    def objekt(self):
        """
        :Attribute: :class:`.Objekt` of the Area
        """
        objekttype = self.data['vegobjekt']['type']
        nvdb_id = self.data['vegobjekt']['id']
        return Objekt(objekttype, nvdb_id)

class Objekt(Nvdb):
    """ Class for individual nvdb-object. """
    def __init__(self, objekt_type, nvdb_id):
        super(Objekt, self).__init__()
        self.objekt_type = objekt_type
        self.nvdb_id = nvdb_id
        self.data = None


    @property
    def egengeometri(self):
        """
        :Attribute: Well Known Text
        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
        if 'geometri' in self.data:
            if self.data['geometri']['egengeometri'] == 'true':
                egengeometri = True
            else:
                egengeometri = False
        return egengeometri

    @property
    def egenskaper(self):
        """
        :Attribute: List of Dict

        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
        if 'egenskaper' in self.data:
            egenskaper = self.data['egenskaper']
        else:
            egenskaper = None
        return egenskaper

            
    @property
    def metadata(self):
        """
        :Attribute: Dict

        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
        if 'metadata' in self.data:
            metadata = self.data['metadata']
        else:
            metadata = None
        return self.data['metadata']


    @property
    def geometri(self):
        """
        :Attribute: Dict

        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
        if 'geometri' in self.data:
            geometri = self.data['geometri']['wkt']
        else:
            geometri = None
        return geometri

    def dump(self, format='json'):
        """
        Function for dumping raw API-result for object.

        :param format: Type of data to dump as. json or xml
        :type format: string
        :returns: str
        """
        if format.lower() == 'json':
            if not self.data:
                self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
            return self.data
        elif format.lower() == 'xml':
            xml_data = self._fetch_data('vegobjekter/{}/{}.xml'.format(self.objekt_type, self.nvdb_id), format='xml')
            return xml_data

    @property
    def foreldre(self):
        """
        :Attribute: List of :class:`.Objekt`

        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
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
        """
        :Attribute: List of :class:`.Objekt`

        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
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
        """
        :Attribute: Dict

        """
        if not self.data:
           self.data = self._fetch_data('vegobjekter/{}/{}'.format(self.objekt_type, self.nvdb_id))
        vegreferanser = []
        if 'lokasjon' in self.data and 'vegreferanser' in self.data['lokasjon']:
            for i in  self.data['lokasjon']['vegreferanser']:
                vegreferanser.append(Vegreferanse(i['kortform']))
        else:
            vegreferanser = None
        return vegreferanser

class Objekt_type(Nvdb):
    """ Class for individual nvdb-object types. (Data catalogue) """
    def __init__(self, objekt_type, meta=None):
        super(Objekt_type, self).__init__()
        self.objekt_type = objekt_type
        self.data = None
        self.meta = meta

    def dump(self, format='json'):
        """
        Function for dumping raw API-result for object.

        :param format: Type of data to dump as. json or xml
        :type format: string
        :returns: str
        """
        if format.lower() == 'json':
            if not self.data:
                self.data = self._fetch_data('vegobjekttyper/{}'.format(self.objekt_type))
            return self.data
        
        elif format.lower() == 'xml':
            xml_data =self._fetch_data('vegobjekttyper/{}.xml'.format(self.objekt_type), format='xml')
            return xml_data

    @property
    def relasjonstyper(self):
        """
        :Attribute: Dict
        """
        if not self.data:
            self.data = self._fetch_data('vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['relasjonstyper']

    @property
    def egenskapstyper(self):
        """
        :Attribute: Dict
        """
        if not self.data:
            self.data = self._fetch_data('vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['egenskapstyper']
    
    @property
    def styringsparametere(self):
        """
        :Attribute: Dict
        """
        if not self.data:
            self.data = self._fetch_data('vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['styringsparametere']

    @property
    def metadata(self):
        """
        :Attribute: Dict
        """
        if self.meta:
            return self.meta
        elif not self.data:
            self.data = self._fetch_data('vegobjekttyper/{}'.format(self.objekt_type))
            metadata = self.data.copy()
            del metadata['egenskapstyper']
            del metadata['relasjonstyper']
            del metadata['styringsparametere']
            self.meta = metadata
        return self.meta

    @property
    def barn(self):
        """
        :Attribute: list of :class:`.Objekt_type`
        """
        if not self.data:
            self.data = self._fetch_data(self, self.baseUrl, 'vegobjekttyper', self.objekt_type)
        realasjoner = self.data['relasjonstyper']
        return [Objekt_type(i['type']['id']) for i in realasjoner['barn']]
    @property
    def foreldre(self):
        """
        :Attribute: list of :class:`.Objekt_type`
        """
        if not self.data:
            self.data = self._fetch_data(self, self.baseUrl, 'vegobjekttyper', self.objekt_type)
        realasjoner = self.data['relasjonstyper']
        return [Objekt_type(i['type']['id']) for i in realasjoner['foreldre']]
    
class Vegreferanse(Nvdb):
    """ Class for working with road refferences. """
    def __init__(self, vegreferanse, meta=None):
        super(Vegreferanse, self).__init__()
        self.vegreferanse = vegreferanse
        self.data = meta
       
    @property
    def detaljert(self):
        """
        :Attribute: Dict
        """
        if not self.data:
            self.data = self._fetch_data('veg', payload={'vegreferanse':self.vegreferanse})
        return self.data['vegreferanse']
        
    @property
    def veglenke(self):
        """
        :Attribute: Dict
        """
        if not self.data:
           self.data = self._fetch_data('veg', payload={'vegreferanse':self.vegreferanse})
        return self.data['veglenke']
    
    @property
    def geometri(self):
        """
        :Attribute: Well known text
        """
        if not self.data:
           self.data = self._fetch_data('veg', payload={'vegreferanse':self.vegreferanse})
        return self.data['geometri']['wkt']
    
    def __str__(self):
        return '{}'.format(self.vegreferanse)
       
class Posisjon(Nvdb):
    """ Class for connecting coordinates to road refferences """
    def __init__(self, payload):
        super(Posisjon, self).__init__()
        self.data = self._fetch_data('posisjon',payload)
    
    @property
    def vegreferanse(self):
        """
        :Attribute: :class:`.Vegreferanse`
        """
        return Vegreferanse(self.data[0]['vegreferanse']['kortform'])
