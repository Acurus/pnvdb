class Objekt(Nvdb):
    """ Class for individual nvdb-objects. """
    def __init__(self, objekt_type, nvdb_id):
        super(Objekt, self).__init__()
        self.objekt_type = objekt_type
        self.nvdb_id = nvdb_id
        self.data = None


    @property
    def egengeometri(self):
        """
        :Attribute: Well known text

        

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
        :Attribute: Dict

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
        :Attribute: List of Objekt

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
        :Attribute: List of Objekt

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