# -*- coding: utf-8 -*-
""" Provide  the ObjektType class """
import json
import logging

from .util import _fetch_data, build_name2id


class ObjektType(object):
    """ Class for individual nvdb-object types. (Data catalogue) """

    def __init__(self, nvdb, objekt_type, meta=None):
        self.nvdb = nvdb
        if isinstance(objekt_type, int):
            self.objekt_type = objekt_type
        else:
            if isinstance(self.nvdb.name2id, dict):
                self.objekt_type = self.nvdb.name2id['nvdb_objekter'][objekt_type.lower()]
            else:
                build_name2id(self.nvdb)
                try:
                    self.objekt_type = self.nvdb.name2id['nvdb_objekter'][objekt_type.lower()]
                except KeyError:
                    logging.error('Objekt_type not found: {}'.format(objekt_type))
                    return None
        
        self.data = None
        self.metadata
        logging.debug("Initialized: ObjektType({})".format(self.objekt_type))

    def __repr__(self):
        return "ObjektType({})".format(self.objekt_type)

    def dump(self, file_format='json'):
        """
        Function for dumping raw API-result for object.

        :param file_format: Type of data to dump as. json or xml
        :type file_format: string
        :returns: str
        """
        if file_format.lower() == 'json':
            if not self.data:
                self.data = _fetch_data(self.nvdb, 'vegobjekttyper/{}'
                                        .format(self.objekt_type))
            return self.data

        elif file_format.lower() == 'xml':
            xml_data = _fetch_data(self.nvdb, 'vegobjekttyper/{}.xml'
                                   .format(self.objekt_type), file_format='xml')
            return xml_data

    @property
    def relasjonstyper(self):
        """
        :Attribute type: Dict
        :keys: ['barn', 'foreldre']
        :keys in keys: ['type', 'relasjonstype', 'id']

        """
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['relasjonstyper']

    def egenskapstype(self, egenskapstype_id=None):
        """
        Function for returning egenskap based on id

        :param egenskaps_id: Id of the property type you want returned
        :type egenskaps_id: int
        :returns: dict unless property is not found. Then None is returned.
        """
        egenskapstype = list(
            filter(lambda x: x['id'] == egenskapstype_id, self.egenskapstyper))
        if len(egenskapstype):
            return egenskapstype[0]
        return None

    @property
    def egenskapstyper(self):
        """
        :Attribute type: list of Dicts
        :keys: ['liste', 'navn', 'datatype_tekst', 'veiledning', 'beskrivelse', 'sensitivitet',
                'sosinvdbnavn', 'objektliste_dato', 'feltlengde', 'sorteringsnummer', 'id',
                'styringsparametere', 'viktighet', 'viktighet_tekst', 'datatype']
        """
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['egenskapstyper']

    @property
    def styringsparametere(self):
        """
        :Attribute type: Dict
        :keys: ['abstrakt_type', 'sideposisjon_relevant', 'retning_relevant', 'ajourhold_splitt',
                'må_ha_mor', 'avledet', 'sektype_20k', 'er_dataserie', 'høyde_relevant', 
                'dekningsgrad', 'overlapp, 'filtrering', 'flyttbar', 'tidsrom_relevant', 
                'ajourhold_i', 'kjørefelt_relevant']
        """
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['styringsparametere']

    @property
    def metadata(self):
        """
        .. todo:: Possible bug. Returns None after reading other attributes

        :Attribute type: Dict
        :keys: ['navn', 'veiledning', 'beskrivelse', 'objektliste_dato', 'sosinvdbnavn', 
                'sorteringsnummer', 'stedfesting', 'id', 'kategorier']
        """
        #if self.meta:
        #    return self.meta
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
            metadata = self.data.copy()
            del metadata['egenskapstyper']
            del metadata['relasjonstyper']
            del metadata['styringsparametere']
            self.meta = metadata
        return self.meta

    @property
    def barn(self):
        """
        :Attribute type: list of :class:`.ObjektType`
        """
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        realasjoner = self.data['relasjonstyper']
        return [ObjektType(self.nvdb, i['type']['id']) for i in realasjoner['barn']]

    @property
    def foreldre(self):
        """
        :Attribute type: list of :class:`.ObjektType`
        """
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        realasjoner = self.data['relasjonstyper']
        return [ObjektType(self.nvdb, i['type']['id']) for i in realasjoner['foreldre']]

    def i_objekt_lista(self):
        """
        Function checking of an object type is part of "Objektlista"

        :returns: bool
        """
        if not self.data:
            self.data = _fetch_data(
                self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        if 'objektliste_dato' in self.data:
            return True
        else:
            return False
