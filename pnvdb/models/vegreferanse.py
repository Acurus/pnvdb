# -*- coding: utf-8 -*-
""" Provide the Vegreferanse class """
from .util import _fetch_data
import logging


class Vegreferanse(object):
    """ Class for working with road refferences.
    """

    def __init__(self, nvdb, vegreferanse):
        self.vegreferanse = vegreferanse
        self.nvdb = nvdb
        
        self.data = None
        logging.debug('Initialized vegreferanse: {}'.format(self.vegreferanse))
        
    def _update_data(self):
        self.data = _fetch_data(self.nvdb, 'veg', payload={
                            'vegreferanse': self.vegreferanse})

    @property
    def fylke(self):
        """
        The county of the road refference
        :Attribute type: int
        """
        if not self.data:
            self._update_data()

        return self.data['vegreferanse']['fylke']
    
    @property
    def kommune(self):
        """
        The kommune of the road refference
        :Attribute type: int
        """
        if not self.data:
            self._update_data()
            
        return self.data['vegreferanse']['kommune']
    
    @property
    def kategori(self):
        """
        The kategori of the road refference
        :Attribute type: String
        """
        if not self.data:
            self._update_data()
            
        return self.data['vegreferanse']['kategori']
    
    @property
    def status(self):
        """
        The status of the road refference
        :Attribute type: String
        """
        if not self.data:
            self._update_data()
            
        return self.data['vegreferanse']['status']
    
    @property
    def nummer(self):
        """
        The nummer of the road refference
        :Attribute type: int
        """
        if not self.data:
            self._update_data()
            
        return self.data['vegreferanse']['nummer']
    
    @property
    def hp(self):
        """
        The hp of the road refference
        :Attribute type: int
        """
        if not self.data:
            self._update_data()
            
        return self.data['vegreferanse']['hp']
    
    @property
    def meter(self):
        """
        The meter of the road refference
        :Attribute type: int
        """
        if not self.data:
            self._update_data()
            
        return self.data['vegreferanse']['meter']
    
    @property
    def geometri(self):
        if not self.data:
            self._update_data()
            
        return self.data['geometri']['wkt']

    @property
    def xyz(self):
        import re
        if not self.data:
            self._update_data()
            
        wkt = self.data['geometri']['wkt']
        reg_res = re.findall(r'\d+\.?\d*', wkt)
        if len(reg_res) < 3:
            x,y = reg_res
            z = None
        else:
            x,y,z = reg_res
        return x,y,z
    
    def __repr__(self):
        return '{}'.format(self.vegreferanse)