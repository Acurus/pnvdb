# -*- coding: utf-8 -*-
""" Contains various helper functions """
import requests
from .. import config
from ..const import NAME2ID
import json

from .pnvdb_exceptions import ApiError, read_api_error


def _fetch_data(nvdb, url_add, payload=None, file_format='json'):
    base_url = config.base_url
    if nvdb:
        headers = nvdb.headers
    else:
        headers = None
    url = '{base_url}/{url_add}'.format(base_url=base_url, url_add=url_add)
    resp = requests.get(url, params=payload, headers=headers)

    # print(resp.headers) # For debugging
    # print(resp.url) # For debugging
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
        print(resp.url)
        raise ApiError(read_api_error(resp))

def update_name2id():
    data = _fetch_data(None, 'vegobjekttyper')
    status = _fetch_data(None, 'status')
    
    name2id = {}
    for objekt in data:
        name2id[objekt['navn'].lower()] = objekt['id']
    with open("pnvdb/const.py",'w') as f:
        f.write('last_seen_version =  {}\n\n'.format(status['datakatalog']['versjon']))
        f.write('NAME2ID = ')
        json.dump(name2id, f,indent=4)

def name2id(objekt_type):
    """
    Funktion that tries to find a objekt_type id from name
    
    :param objekt_type: The name that should be converted

    :type objekt_type: string
    :returns: int
    """
    try:
        objekt_id = NAME2ID[objekt_type.lower()]
    except:
        print('Not found')
    return objekt_id
        
        
        
        



