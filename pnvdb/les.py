# -*- coding: utf-8 -*-
from . import models
from .models.util import _fetch_data


class Nvdb(object):
    """ The main class for interfacing with the API.

        :param client: Name of client using the API
        :type client: str
        :param contact: Contact information of user of the API
        :type contact: str
        :returns:  Nvdb Class

        :usage:

        >>> import pnvdb
        >>> nvdb = pnvdb.Nvdb(client='Your-App-Name', contact='Your-contact-information')

    """

    def __init__(self, client='pnvdb', contact=''):
        self.base_url = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client, 'X-Kontaktperson': contact}
        self.srid = ''
        self.antall = 1000

    def _generator(self, url, _payload, objekt_type, data):
        while True:
            returnert = data['metadata']['returnert']
            if returnert == 0:
                break

            _payload.update({'start':data['metadata']['neste']['start']})
            for obj in enumerate(data['objekter']):
                yield models.Objekt(self, objekt_type, obj[1]['id'], obj)
            data = _fetch_data(self, url, _payload)

    def status(self):
        """ Method for getting information about the current status of the API

            :returns: Dict
            :keys: ['datakatalog', 'datagrunnlag']

            :usage:

            >>> status = nvdb.status()
            >>> print(status['datakatalog']['versjon'])
            2.10


        """
        return _fetch_data(self, 'status')

    def objekt(self, objekt_type, nvdb_id):
        """ Method for creating a spesific nvdb python Objekt

            :param objekt_type: nvdb objekttype id.
            :type objekt_type: int
            :param nvdb_id: the unique nvdb id
            :type nvdb_id: int
            :returns: :class:`.Objekt`

            :usage:

            >>> obj = nvdb.objekt(objekt_type=67, nvdb_id=89204552)
            >>> print(obj.metadata)
            {'versjon': 3, 'type':P {'navn': 'Tunnelløp', 'id': 67}, 'startdato': '2014-01-17',
             'sist_modifisert': '2017-10-23 15:15:50'}

        """
        return models.Objekt(self, objekt_type, nvdb_id)


    def objekt_type(self, objekt_type):
        """ Method for creating a spesific nvdb python

            :param objekt_type: nvdb objekttype id.
            :type objekt_type: int
            :returns: :class:`.ObjektType`

            :usage:

            >>> obj = nvdb.objekt_type(objekt_type=67)
            >>> print(obj.metadata['sosinvdbnavn'])
            Tunnelløp_67
        """
        return models.ObjektType(self, objekt_type)


    def objekt_typer(self):
        """ Returns objekt_type of every avaliable obj type in nvdb

            :returns: List of :class:`.ObjektType`

            :usage:

            >>> obj_types = nvdb.objekt_typer()
            >>> print(obj_types[0].metadata['sosinvdbnavn'])
            Skjerm_3

        """
        data = _fetch_data(self, 'vegobjekttyper')
        objekt_typer = []
        for objekt_type in data:
            objekt_type_id = objekt_type['id']
            objekt_typer.append(models.ObjektType(self, objekt_type_id, meta=objekt_type))
        return objekt_typer


    def hent(self, objekt_type, kriterie=None):
        """ Return a generator object that can be itterated over
            to fetch the results of the query.

            :param objekt_type: nvdb objekttype id.
            :type objekt_type: int
            :param payload: filters for the query
            :type payload: dict
            :returns: generator of :class:`.Objekt`

            :usage:

            >>> criteria = {'fylke':'2','egenskap':'1820>=20'}
            >>> bomstasjoner = nvdb.hent(45, kriterie=criteria)
            >>> for bomstasjon in bomstasjoner:
            >>>     print(bomstasjon)
        """
        _payload = dict()
        if kriterie:
            _payload = kriterie.copy()
        _payload.update({'antall':self.antall, 'segmentering':'false', 'inkluder':'alle'})
        
        url = 'vegobjekter/{objekt_type}'.format(objekt_type=objekt_type)
        data = _fetch_data(self, url, payload=_payload)
        if data['metadata']['returnert'] == 0:
            return None
        else:
            return self._generator(url, _payload, objekt_type, data)
       
    def vegreferanse(self, vegreferanse):
        """ Return vegreferanse object.
            PS : Only support point refferences

            :param vegreferanse: The road refferences to objectify
            :type vegreferanse: string
            :returns: :class:`.Vegreferanse`

            :usage:

            >>> print(nvdb.vegreferanse('1600Ev6hp12m1000'))
        """
        if isinstance(vegreferanse, list):
            return [models.Vegreferanse(self, vegref)
                    for vegref in vegreferanse]
        return models.Vegreferanse(self, vegreferanse)


    def posisjon(self, x_coordinate=None, y_coordinate=None, lat=None, lon=None):
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

            :usage:

            >>> pos = nvdb.posisjon(x=269815,y=7038165)
            >>> print(pos.vegreferanse)
        """
        if x_coordinate and y_coordinate:
            payload = {'nord':y_coordinate, 'ost':x_coordinate}
        elif lat and lon:
            payload = {'lat':lat, 'lon':lon}

        return models.Posisjon(self, payload)


    def regioner(self):
        """ Returns an Area object for all regions

            :returns: list of :class:`.Area`

            :usage:

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = _fetch_data(self, 'omrader/regioner', payload)
        return [models.Area(self, models.Area_data) for models.Area_data in data]

    def fylker(self):
        """ Returns an mArea object for all fylker

            :returns: list of :class:`.Area`

            :usage:

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = _fetch_data(self, 'omrader/fylker', payload)
        return [models.Area(self, models.Area_data) for models.Area_data in data]

    def vegavdelinger(self):
        """ Returns an Area object for all vegavdelinger

            :returns: list of :class:`.Area`

            :usage:

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = _fetch_data(self, 'omrader/vegavdelinger', payload)
        return [models.Area(self, models.Area_data) for models.Area_data in data]

    def kommuner(self):
        """ Returns an Area object for all kommuner

            :returns: list of :class:`.Area`

            :usage:

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = _fetch_data(self, 'omrader/kommuner', payload)
        return [models.Area(self, models.Area_data) for models.Area_data in data]

    def kontraktsomrader(self):
        """ Returns an Area object for all kontraktsomrader

            :returns: list of :class:`.Area`

            :usage:

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = _fetch_data(self, 'omrader/kontraktsomrader', payload)
        return [models.Area(self, models.Area_data) for models.Area_data in data]

    def riksvegruter(self):
        """ Returns an Area object for all riksvegruter

            :returns: list of :class:`.Area`

            :usage:

            >>> for region in nvdb.regioner():
            >>>     print(region.metadata)
        """
        payload = {'inkluder':'alle'}
        data = _fetch_data(self, 'omrader/riksvegruter', payload)
        return [models.Area(self, models.Area_data) for models.Area_data in data]
