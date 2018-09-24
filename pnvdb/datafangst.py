import json

from . import config, models

class Datafangst(object):
    """ Main class for interfacing with the 'Datafangst' API

        :param username: Datafangst username
        :type username: str
        :param password: Datafangst password
        :type password: str
        :param contractId: Datafangst contract ID
        :type contractId: str
        :returns: :class:`.Datafangst`

        :usage:

        >>> import pnvdb
        >>> datafangst = pnvdb.Datafangst(username, password, contractId)

    """
    def __init__(self, username=None, password=None, contractId=None):
        self.base_url = config.datafangst_base_url
        self.username = username
        self.password = password
        self.headers = {
            'Content-Type': "application/geo+json",
            'Accept': "application/json"
        }
        self.url = "{baseurl}/{contractId}/featurecollection".format(
            baseurl=self.base_url, contractId=contractId)

    def feature_collection(self):
        """
        Method for initializing and working with a datafangst feature collection
        
        :returns: :class:`.FeatureCollection`
        """
        return models.FeatureCollection(self.url, self.username, self.password, self.headers)

    def feature(self, objekt_type, coordinates, tag):
        """
        Method for initialzing and working with a datafangst feature
        
        :param objekt_type: NVDB object type of the feature
        :type objekt_type: int
        :param coordinates: Coordinates describing the feature geometry
        :type coordinates: list of tuples or singel tuple for points
        :param tag: Identifying tag for the feature. Identical tags will be made uniqe with a number.
        :type tag: str
        
        :returns: :class:`.Feature`
        """
        return models.Feature(objekt_type, coordinates, tag)
