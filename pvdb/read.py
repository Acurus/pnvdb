import requests
from .core import *

class Read(object):
    'Read NVDB data'
    
    def __init__(self, client='PVDB', contact='jankyr@vegvesen.no'):
        self.baseUrl = 'https://www.vegvesen.no/nvdb/api/v2'
        self.headers = {'X-Client': client,'X-Kontaktperson': contact}
        self.srid = '32633'

    @property
    def status(self):
        status = requests.get('https://www.vegvesen.no/nvdb/api/v2/status')
        return check_response(status)

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
        
        return self._check_response(data)
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
            vegobjekt
            alle
        '''
        params = self._update_params(kwargs)
        urlAdd = 'omrader'
        url = '{baseUrl}/{urlAdd}/{area_type}/'.format(baseUrl=self.baseUrl,
            urlAdd=urlAdd, area_type=area_type)
        data = requests.get(url, params = params, headers=self.headers)
        return self._check_response(data)
    
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