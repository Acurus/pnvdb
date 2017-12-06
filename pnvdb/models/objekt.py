# -*- coding: utf-8 -*-
""" Provide the Objekt class """
from .util import _fetch_data
from .vegreferanse import Vegreferanse

class Objekt(object):
    """ Class for individual nvdb-objects. """
    def __init__(self, nvdb, objekt_type, nvdb_id):
        self.nvdb = nvdb
        self.objekt_type = objekt_type
        self.nvdb_id = nvdb_id
        self.data = None

    @property
    def egengeometri(self):
        """
        Boolean value that tell if the object has egengeometri or not.

        :Attribute type: Bool
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        return bool(self.data['geometri']['egengeometri'] == 'true')
    

    def egenskap(self, egenskaps_id=None):
        """
        Function for returning egenskap based on id

        :param egenskaps_id: Id of the property type you want returned
        :type egenskaps_id: int
        :returns: dict unless property is not found. Then None is returned.
        """
        egenskap = list(filter(lambda x: x['id'] == egenskaps_id, self.egenskaper))
        if len(egenskap):
            return egenskap[0]
        return None

    @property
    def egenskaper(self):
        """
        :Attribute type: List of Dict
        :keys: ['datatype_tekst', 'id', 'datatype', 'verdi', 'navn']
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        if 'egenskaper' in self.data:
            egenskaper = self.data['egenskaper']
        else:
            egenskaper = None
        return egenskaper

            
    @property
    def metadata(self):
        """
        :Attribute type: Dict
        :keys: ['versjon', 'sist_modifisert', 'startdato', 'type']
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        if 'metadata' in self.data:
            metadata = self.data['metadata']
        else:
            metadata = None
        return metadata


    @property
    def geometri(self):
        """
        :Attribute type: Well Known Text
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        if 'geometri' in self.data:
            geometri = self.data['geometri']['wkt']
        else:
            geometri = None
        return geometri

    def dump(self, file_format='json'):
        """
        Function for dumping raw API-result for object.

        :param file_format: Type of data to dump as. json or xml
        :type file_format: string
        :returns: str
        """
        if file_format.lower() == 'json':
            if not self.data:
                self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                        .format(self.objekt_type, self.nvdb_id))
            return self.data
        elif file_format.lower() == 'xml':
            xml_data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}.xml'
                                   .format(self.objekt_type, self.nvdb_id), file_format='xml')
            return xml_data

    @property
    def foreldre(self):
        """
        :Attribute type: List of :class:`.Objekt`
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        foreldre = []
        if 'relasjoner' in self.data and 'foreldre' in self.data['relasjoner']:
            for i in self.data['relasjoner']['foreldre']:
                objekt_type = i['type']['id']
                for nvdb_id in i['vegobjekter']:
                    foreldre.append(Objekt(self.nvdb, objekt_type, nvdb_id))
        else:
            foreldre = None
        return foreldre

    @property
    def barn(self):
        """
        :Attribute type: List of :class:`.Objekt`

        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        barn = []
        if 'relasjoner' in self.data and 'barn' in self.data['relasjoner']:
            for i in self.data['relasjoner']['barn']:
                objekt_type = i['type']['id']
                for nvdb_id in i['vegobjekter']:
                    barn.append(Objekt(self.nvdb, objekt_type, nvdb_id))

        else:
            barn = None
        return barn

    @property
    def vegreferanser(self):
        """
        :Attribute type: :class:`.Vegreferanse`

        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        vegreferanser = []
        if 'lokasjon' in self.data and 'vegreferanser' in self.data['lokasjon']:
            for i in  self.data['lokasjon']['vegreferanser']:
                vegreferanser.append(Vegreferanse(self.nvdb, i['kortform']))
        else:
            vegreferanser = None
        return vegreferanser
    @property
    def stedfestinger(self):
        """
        :Attribute type: list of dict
        :keys: []

        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekter/{}/{}'
                                    .format(self.objekt_type, self.nvdb_id))
        return data['stedfestinger']