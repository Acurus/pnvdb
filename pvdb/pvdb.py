import requests
from .pvdb_exceptions import ResponseError
class PvdbRead:
    "Read NVDB data"
    
    def __init__(self):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {"X-Client": "PVDB","X-Kontaktperson": "jankyr@vegvesen.no"}
        self.segmentation = 'true'
        self.srid = '32633'
    
    def _update_params(self, params):
        params.update({'srid':self.srid, 'segmentering':self.segmentation})
        return params

    def _check_response(self, resp):
        '''Function verifes that a 200 code was returned from the API
        and returns the data as Json.

        If a 200 code was not returned, it tries to return the error recived 
        from the API.'''
        
        if resp.status_code == requests.codes.ok:
            return resp.json()
        else:
            try:
                resp = resp.json()[0]
                raise ResponseError(resp['message'])
            
            except:
                raise

    def get_object_list(self):
        
        urlAdd = 'vegobjekter/'
        url = '{baseUrl}/{urlAdd}'.format(baseUrl=self.baseUrl, urlAdd=urlAdd)
        
        data = requests.get(url, headers=self.headers)
        data = self.check_response(data)

        for i in data:
            i['id'] = i['href'].split('/')[-1]

        return data

    def get_road_objects(self, obj, **kwargs):
        ''' Function for finding road objects based on type.
            obj : 
                The object type id. 
            
            params a dictionary of values: 
                inkluder : Comma seperated list of information elements
                to return in addtion to the objects unique id.
                values : [metadata, egenskaper, relasjon, lokasjon, vegsegmenter, geomteri, alle]
                
                srid : geografic refference system. 
                controlled by class
                default = 32633

                geometritoleranse : Weather to return simplified geometry. if the paramter
                is left out, full geometry is returned. The number represent the tollerance for 
                generating the simplified geometry. 
                Values : [10, 20, 30]

                segmentering : Wether line objects should be segmented based on search area.
                Values : [true, false]
                controlled by class
                default = true
        '''

        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}'.format(baseUrl=self.baseUrl, urlAdd=urlAdd, obj=obj)
        params = self._update_params(kwargs)
        data = requests.get(url, params = params, headers=self.headers)
        print(data.url)
        return self._check_response(data)
    
    def get_road_object(self, obj, objectID, **kwargs):
        '''
        Function for finding objects based on unique id.
            obj : 
                The object type id.
            objectID : 
                unique object id for the object type.
        '''
        params = self._update_params(kwargs)
        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}/{objectID}'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, obj=obj, objectID=objectID, params = params)
        
        data = requests.get(url)
        
        return self.check_response(data)

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

    def get_road_links(self, **kwargs):
        '''
        Function for getting the topological road network from NVDB
        '''
        params = self._update_params(kwargs)
        urlAdd = 'vegnett/lenker'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url)
        return self.check_response(data)

    def get_areas(self,area_type, **kwargs):
        '''
        Function for getting areas defined in NVDB based on type.
        area_type : 
            regioner
            fylker
            vegavdelinger
            kommuner
            kontraktsomrader
            riksveiruter
        include : 
            kartutsnitt
            senterpunkt
            vegobjekttyper
            alle
        '''
        params = self._update_params(kwargs)
        urlAdd = 'omrader'
        url = '{baseUrl}/{urlAdd}/{area_type}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, area_type=area_type)
        data = requests.get(url, params = params, headers=self.headers)
        return self.check_response(data)
    
    def get_position(self, **Kwargs):
        '''
        Function for getting closest road to position.
        
        params : 
            nord                <flyttall>  Østlig koordinat
            ost                 <flyttall>  Nordlig koordinat
            lat                 <flyttall>  Breddegrad
            lon                 <flyttall>  Lengdegrad
            maks_avstand        <heltall>   Angir søkeavstand i meter. 
            Default: 30
            maks_antall         <heltall>   Angir hvor mange resultater som maksimum skal returneres. 
            Default: 1
            konnekteringslenker true
                                false       Angir om det skal returneres treff på konnekteringslenker. 
                                            Default: false
            detaljerte_lenker   true
                                false       Angir om det skal returneres treff på detaljerte vegnettsnivå. 
                                            Default: false
            vegreferanse        vegreferanse    Angi om det kun skal søkes innenfor spesifikke vegreferanser
            srid                srid        Angir hvilket geografisk referansesystem geometrien skal returneres i.
                                            Default: 32633

        '''
        params = self._update_params(kwargs)
        urlAdd = 'posisjon'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, params = params, headers=self.headers)
        return self.check_response(data)
    
    def get_road(self, **kwargs):
        '''
        TODO : Add batch functionallity

        This function can be used for doing a query on roadlink or road refferance, 
        and get a coresponding point on the roadnet with coordinate, road refference and road link.

        params : 

                vegreferanse    vegreferanse    Angir vegreferanse som punkt på vegnettet.
                veglenke        veglenke        Angir veglenke som punkt på vegnettet.
                srid            srid            Angir hvilket geografisk referansesystem geometrien skal returneres i.
                                                Default: 32633
        '''
        params = self._update_params(kwargs)
        urlAdd = 'veg'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, params = params, headers=self.headers)
        return self.check_response(data)

    def get_status(self):
        ''' Function for getting status parameters about the API.

        '''
        urlAdd = 'status'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, headers=self.headers)
        return self.check_response(data)
        
class PvdbWrite:
    "Write NVDB data"
    def __init__(self):
        pass