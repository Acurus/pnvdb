from .util import _fetch_data
from .vegreferanse import Vegreferanse

class Posisjon(object):
    """ Class for connecting coordinates to road refferences """
    def __init__(self, nvdb, payload):
        super(Posisjon, self).__init__()
        self.nvdb = nvdb
        self.data = _fetch_data(self.nvdb, 'posisjon',payload)
        
    
    @property
    def vegreferanse(self):
        """
        :Attribute type: :class:`.Vegreferanse`
        """
        return Vegreferanse(self.nvdb, self.data[0]['vegreferanse']['kortform'])
