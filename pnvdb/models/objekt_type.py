# -*- coding: utf-8 -*-
from .util import _fetch_data


class Objekt_type(object):
    """ Class for individual nvdb-object types. (Data catalogue) """
    def __init__(self, nvdb, objekt_type, meta=None):
        super(Objekt_type, self).__init__()
        self.nvdb = nvdb
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
                self.data = _fetch_data(self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
            return self.data
        
        elif format.lower() == 'xml':
            xml_data =_fetch_data(self.nvdb, 'vegobjekttyper/{}.xml'.format(self.objekt_type), format='xml')
            return xml_data

    @property
    def relasjonstyper(self):
        """
        :Attribute type: Dict
        :keys: ['barn', 'foreldre']
        :keys in keys: ['type', 'relasjonstype', 'id']

        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['relasjonstyper']

    @property
    def egenskapstyper(self):
        """
        :Attribute type: list of Dicts
        :keys: ['liste', 'navn', 'datatype_tekst', 'veiledning', 'beskrivelse', 'sensitivitet',
                'sosinvdbnavn', 'objektliste_dato', 'feltlengde', 'sorteringsnummer', 'id',
                'styringsparametere', 'viktighet', 'viktighet_tekst', 'datatype']
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['egenskapstyper']
    
    @property
    def styringsparametere(self):
        """
        :Attribute type: Dict
        :keys: ['abstrakt_type', 'sideposisjon_relevant', 'retning_relevant', 'ajourhold_splitt',
                'må_ha_mor', 'avledet', 'sektype_20k', 'er_dataserie', 'høyde_relevant', 'dekningsgrad',
                'overlapp, 'filtrering', 'flyttbar', 'tidsrom_relevant', 'ajourhold_i', 'kjørefelt_relevant']
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
        return self.data['styringsparametere']

    @property
    def metadata(self):
        """
        .. todo:: Possible bug. Returns None after reading other attributes

        :Attribute type: Dict
        :keys: ['navn', 'veiledning', 'beskrivelse', 'objektliste_dato', 'sosinvdbnavn', 'sorteringsnummer',
                'stedfesting', 'id', 'kategorier']
        """
        if self.meta:
            return self.meta
        elif not self.data:
            self.data = _fetch_data(self.nvdb, 'vegobjekttyper/{}'.format(self.objekt_type))
            metadata = self.data.copy()
            del metadata['egenskapstyper']
            del metadata['relasjonstyper']
            del metadata['styringsparametere']
            self.meta = metadata
        return self.meta

    @property
    def barn(self):
        """
        :Attribute type: list of :class:`.Objekt_type`
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, self.baseUrl, 'vegobjekttyper', self.objekt_type)
        realasjoner = self.data['relasjonstyper']
        return [Objekt_type(i['type']['id']) for i in realasjoner['barn']]
    @property
    def foreldre(self):
        """
        :Attribute type: list of :class:`.Objekt_type`
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, self.baseUrl, 'vegobjekttyper', self.objekt_type)
        realasjoner = self.data['relasjonstyper']
        return [Objekt_type(self.nvdb, i['type']['id']) for i in realasjoner['foreldre']]