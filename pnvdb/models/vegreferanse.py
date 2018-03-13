# -*- coding: utf-8 -*-
""" Provide the Vegreferanse class """
from .util import _fetch_data

class Vegreferanse(object):
    """ Class for working with road refferences.
        Does not handle links as of now due to limitations in the API
    """
    def __init__(self, nvdb, vegreferanse):
        self.vegreferanse = vegreferanse
        self.nvdb = nvdb
        self.fra_data = None
        self.til_data = None

        if self.vegreferanse.find('-') != -1: # Check if the refference is a stretch
            self.fra_meter, self.til_meter = [int(value) for value in self.vegreferanse.split('m')[1].split('-')]
            self.lengde = self.til_meter - self.fra_meter
        else:
            self.lengde = 0

    def __repr__(self):
        return '{}'.format(self.vegreferanse)

    @property
    def start(self):
        """
        The start of the road refference
        :Attribute type: Dict
        :keys: ['geometri', 'veglenke', 'vegreferanse']
        """
        if not self.fra_data:
            if self.lengde:
                vegreferanse = '{}m{}'.format(self.vegreferanse.split('m')[0], self.fra_meter)
                self.fra_data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':vegreferanse})
            else:
                self.fra_data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':self.vegreferanse})
        return self.fra_data

    @property
    def slutt(self):
        """
        The end of the road refference
        :Attribute type: Dict
        :keys: ['geometri', 'veglenke', 'vegreferanse']
        """
        if not self.til_data:
            if self.lengde:
                vegreferanse = '{}m{}'.format(self.vegreferanse.split('m')[0], self.til_meter)
                self.til_data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':vegreferanse})
            else:
                self.til_data = _fetch_data(self.nvdb, 'veg', payload={'vegreferanse':self.vegreferanse})
        return self.til_data
    
      
