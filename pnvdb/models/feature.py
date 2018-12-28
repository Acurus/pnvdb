import geojson

from ..les import Nvdb


class Feature(object):
    '''Class for defining objects ready to push to Datafangst'''

    def __init__(self, objekt_type, coordinates, tag):
        self._objekt_type = objekt_type
        self._coordinates = None
        self.properties = {}
        self.coordinates(coordinates)
        self.properties["typeId"] = objekt_type
        self.properties["tag"] = tag
        self.properties["dataCatalogVersion"] = self._current_datakatalog()
        self.properties['attributes'] = {}

    def _current_datakatalog(self):
        """ Returns current datakatalog version """
        status = Nvdb.status(None)
        return status['datakatalog']['versjon']

    def coordinates(self, geometry):
        """ Method for setting the geometry of the feature
            
            :param coordinates: Coordinates describing the feature geometry
            :type coordinates: list of tuples or singel tuple for points
        """
        if isinstance(geometry, list):
            if geometry[0] == geometry[-1]:
                self._coordinates = geojson.Polygon([geometry])
            else:
                self._coordinates = geojson.LineString(geometry)
        else:
            self._coordinates = geojson.Point(geometry)

    def attribute(self, attribute_id, attribute_value):
        """ Method for adding an attribute to the feature
            
            :param attribute_id: nvdb attribute ID
            :type attribute_id: int
            :param attribute_value: value for the attribute
            :type attribute_value: str or int
        """
        self.properties['attributes'][str(attribute_id)] = str(attribute_value)

    def comment(self, comment):
        """ Method for adding an commnet to the feature
            
            :param comment: The comment to add to the feature
            :type comment: str
        """
        self.properties["comment"] = comment

    def tag(self, tag):
        """ Method for adding a tag to the feature
        :param tag: Identifying tag for the feature. Identical tags will be made uniqe with a number.
        :type tag: str
        """
        self.properties["tag"] = tag


    def __repr__(self):
        feature = geojson.Feature(geometry=self._coordinates,
                                  properties=self.properties)
        return geojson.dumps(feature)
