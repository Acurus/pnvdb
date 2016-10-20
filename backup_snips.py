

    def get_road_objectTypes(self, **kwargs):
        '''
        Function for getting objects metadata from the NVDB data catalog.
            parmas : 
                    egenskapstyper
                    relasjonstyper
                    styringsparametere
                    alle
        '''
        params = self._update_params(kwargs)
        urlAdd = 'vegobjekttyper'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, params=params)
        
        data = requests.get(url)
        
        return self.check_response(data)

    def get_road_objectType(self, obj, **kwargs):
        '''
        Function for getting objects metadata from the NVDB data catalog.
            params : 
                    egenskapstyper
                    relasjonstyper
                    styringsparametere
                    alle
        '''
        params = self._update_params(kwargs)
        urlAdd = 'vegobjekttyper'
        url = '{baseUrl}/{urlAdd}/{obj}'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, obj=obj, params=params)
        data = requests.get(url)
        
        return self.check_response(data)


    
    def _status(self):
        ''' Function for getting status parameters about the API.
        '''
        urlAdd = 'status'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, headers=self.headers)
        return self._check_response(data)
        
class PvdbWrite:
    "Write NVDB data"
    def __init__(self):
        pass
