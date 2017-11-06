from .util import _fetch_data

class Vegreferanse(object):
    """ Class for working with road refferences. """
    def __init__(self, nvdb, vegreferanse, meta=None):
        super(Vegreferanse, self).__init__()
        self.vegreferanse = vegreferanse
        self.nvdb = nvdb
        self.data = meta
       
    @property
    def detaljert(self):
        """
        :Attribute: Dict
        """
        if not self.data:
            self.data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':self.vegreferanse})
        return self.data['vegreferanse']
        
    @property
    def veglenke(self):
        """
        :Attribute: Dict
        """
        if not self.data:
           self.data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':self.vegreferanse})
        return self.data['veglenke']
    
    @property
    def geometri(self):
        """
        :Attribute: Well known text
        """
        if not self.data:
           self.data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':self.vegreferanse})
        return self.data['geometri']['wkt']
    
    def __str__(self):
        return '{}'.format(self.vegreferanse)