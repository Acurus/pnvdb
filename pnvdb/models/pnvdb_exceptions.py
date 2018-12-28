# -*- coding: utf-8 -*-
"""Provide the error handling class """


class NvdbError(Exception):
    """Base class for exceptions in this module."""
    pass

class ApiError(NvdbError):
    def __init__(self, message):
        self.message = message

class AutoUpdateError(NvdbError):
    def __init__(self, message):
        self.message = message

def read_api_error(resp):
    try:
        return resp.json()[0]['message']
    except:
        resp.raise_for_status()
