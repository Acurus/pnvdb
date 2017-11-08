
from .util import _fetch_data
from .objekt import Objekt

class Area(object):
    """ Class for area objects. """ 
    def __init__(self, nvdb, area_data):
        super(Area, self).__init__()
        self.nvdb = nvdb
        self.data = area_data

    @property
    def metadata(self):
        """ 
        :Attribute type: Dict
        
        :keys: ['nummer','navn']
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
        :Attribute type: Well Known Text
        """
        if 'kartutsnitt' in self.data:
            return self.data['kartutsnitt']['wkt']
        else:
            return None
    
    
    @property
    def senterpunkt(self):
        """
        :Attribute type: Well Known Text
        """
        if 'senterpunkt' in self.data:
            return self.data['senterpunkt']['wkt']
        else:
            return None
    

    @property
    def objekt(self):
        """
        :Attribute type: :class:`.Objekt` of the Area
        """
        objekttype = self.data['vegobjekt']['type']
        nvdb_id = self.data['vegobjekt']['id']
        return Objekt(self.nvdb, objekttype, nvdb_id)