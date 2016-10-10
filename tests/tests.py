from pvdb import pvdb
import unittest
from unittest.mock import MagicMock

class test_pvdbRead(unittest.TestCase):
    
    def test_pvdbRead_init(self):
        r = pvdb.PvdbRead()
        self.assertEqual(r.srid,'32633')

class test_update_params(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()
    def test_returnvalue_empty(self):
        self.assertEqual(self.r._update_params({}), {'srid':'32633'})
    def test_returnvalue(self):
        self.assertEqual(self.r._update_params({'inkluder':'alle'}),
                                               {'srid':'32633','inkluder':'alle'})

class test_check_response(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_get_objectlist(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()
    def test_get_objectlist(self):
        pass
        #requests = MagicMock(name='method')
        #r = pvdb.PvdbRead()
        #requests.return_value = '{}'
        #r.get_object_list()

class test_get_road_objects(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_get_road_object(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_get_road_objectTypes(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_get_road_objectType(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_get_road_links(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()
class test_get_areas(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_get_position(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_road(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()

class test_status(unittest.TestCase):
    def setUp(self):
        self.r = pvdb.PvdbRead()


if __name__ == '__main__':
    unittest.main()