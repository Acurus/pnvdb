import requests
def update_params(self, params):
        params.update({'srid':self.srid,'antall':5})
        return params

def check_response(resp):
    '''Function verifes that a 200 code was returned from the API
    and returns the data as Json.
    If a 200 code was not returned, it tries to return the error recived 
    from the API.'''
    
    if resp.status_code == requests.codes.ok:
        return resp.json()
    else:
        raise ApiError(read_api_error(resp))

def _test():
    print('hei hei')