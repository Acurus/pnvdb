# -*- coding: utf-8 -*-
""" Contains various helper functions """
import json
import logging

import requests

from .. import config
from .pnvdb_exceptions import ApiError, read_api_error


def _fetch_data(nvdb, url_add, payload=None, file_format='json'):
    """
    function that collects data from the api
    
    :param nvdb: Instance off Nvdb
    :type nvdb: :class:`.Nvdb`
    :param url_add: The API endpoint to fetch
    :type url_add: string
    :param payload: arguments for the api endpoint
    :type payload: string
    :param file_format: one of two values 'json or xml' will return data in this format
    :type file_format: string

    :returns: data as a dictionary
    """
    base_url = config.lesapi_base_url
    if nvdb:
        headers = nvdb.headers
    else:
        headers = None
    url = '{base_url}/{url_add}'.format(base_url=base_url, url_add=url_add)
    resp = requests.get(url, params=payload, headers=headers)

    logging.debug(resp.headers)
    logging.debug(resp.url)
    data = _check_response(resp, file_format)
    return data


def _check_response(resp, file_format='json'):
    """Function verifes that a 200 code was returned from the API
    and returns the data as Json.
    If a 200 code was not returned, it tries to return the error recived 
    from the API."""

    if resp.status_code == 200 and file_format == 'json':
        return resp.json()
    elif resp.status_code == 200 and file_format == 'xml':
        return resp.text
    else:
        raise ApiError(read_api_error(resp))


def build_name2id(nvdb):
    """
    Function that updates nvdb_name2id
    """
    nvdb.name2id = {}
    name_data = _fetch_data(None, 'vegobjekttyper')
    nvdb_objekter = {}
    for objekt in name_data:
        nvdb_objekter[objekt['navn'].lower()] = objekt['id']
    
    nvdb.name2id['nvdb_objekter'] = nvdb_objekter
