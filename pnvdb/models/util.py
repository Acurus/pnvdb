# -*- coding: utf-8 -*-
""" Contains various helper functions """
import requests

from .pnvdb_exceptions import ApiError, read_api_error


def _fetch_data(nvdb, url_add, payload=None, file_format='json'):
    url = '{baseUrl}/{url_add}'.format(baseUrl=nvdb.base_url, url_add=url_add)
    resp = requests.get(url, params=payload, headers=nvdb.headers)

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
