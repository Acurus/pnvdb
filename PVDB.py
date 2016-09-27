import requests

class PvdbRead:
    "Read NVDB data"
    
    def __init__(self):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {"X-Client": "PVDB","X-Kontaktperson": "jankyr@vegvesen.no"}
        self.segmentation = 'true'
        self.srid = '32633'
    
    def check_response(self, resp):
        if True:
            return resp

    def get_road_objects(self, obj, params):
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

        params.update(self.headers,self.segmentation,self.srid)

        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}'.format(baseUrl=self.baseUrl, urlAdd=urlAdd, obj=obj)
        
        data = requests.get(url, params = params, headers=self.headers).json()
        
        return self.check_response(data)
    
    def get_road_object(self, obj, objectID, params):
        '''
        Function for finding objects based on unique id.
            obj : 
                The object type id.
            objectID : 
                unique object id for the object type.
        '''
        params.update(self.paramUpdate)

        urlAdd = 'vegobjekter'
        url = '{baseUrl}/{urlAdd}/{obj}/{objectID}'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, obj=obj, objectID=objectID)
        
        data = requests.get(url).json()
        
        return self.check_response(data)

    def get_road_objectTypes(self, params):
        '''
        Function for getting objects metadata from the NVDB data catalog.
            include : 
                    egenskapstyper
                    relasjonstyper
                    styringsparametere
                    alle
        '''
        urlAdd = 'vegobjekttyper'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, include=include)
        
        data = requests.get(url).json()
        
        return self.check_response(data)

    def get_road_objectType(self, obj, params):
        '''
        Function for getting objects metadata from the NVDB data catalog.
            params : 
                    egenskapstyper
                    relasjonstyper
                    styringsparametere
                    alle
        '''
        urlAdd = 'vegobjekttyper'
        url = '{baseUrl}/{urlAdd}/{obj}'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, obj=obj)
        data = requests.get(url).json()
        
        return self.check_response(data)

    def get_road_links(self, params):
        '''
        Function for getting the topological road network from NVDB
        '''
        urlAdd = 'vegnett/lenker'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url).json()
        return self.check_response(data)

    def get_areas(self,area_type, params):
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
        params.update({'srid':self.srid})
        urlAdd = 'omrader'
        url = '{baseUrl}/{urlAdd}/{area_type}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, area_type=area_type)
        data = requests.get(url, params = params, headers=self.headers).json()
        return self.check_response(data)
    
    def get_position(self,params):
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
        params.update({'srid':self.srid})
        urlAdd = 'posisjon'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, params = params, headers=self.headers).json()
        return self.check_response(data)
    
    def get_road(self, params):
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
        params.update({'srid':self.srid})
        urlAdd = 'veg'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, params = params, headers=self.headers).json()
        return self.check_response(data)

    def get_status(self):
        ''' Function for getting status parameters about the API.

        '''
        urlAdd = 'status'
        url = '{baseUrl}/{urlAdd}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd)
        data = requests.get(url, headers=self.headers).json()
        return self.check_response(data)
        
class PvdbWrite:
        def __init__(self):
            pass