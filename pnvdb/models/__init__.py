# -*- coding: utf-8 -*-
""" Make avaliable the various classes to the API """
from .objekt import Objekt
from .vegreferanse import Vegreferanse
from .area import Area
from .objekt_type import ObjektType
from .posisjon import Posisjon
__all__ = ('Objekt','Vegreferanse', 'Area', 'objekt_type', 'posisjon')