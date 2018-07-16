from pnvdb.var import auth
import pnvdb
import pprint
import json
import geojson

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    username = auth.username
    password = auth.password
    contractId = '7168c19c-e637-48fd-9771-61eb43c53d6f'
    datafangst = pnvdb.Datafangst(username, password, contractId)
    poly = [[10.39241731, 63.43053048],
            [10.39495434, 63.43043698],
            [10.39579151, 63.42898665],
            [10.39272171, 63.42909269],
            [10.39241731, 63.43053048]]

    feature1 = pnvdb.Feature(227,poly,"Forsterkningslag#1")
    feature1.attribute(5543,'2016802')
    feature1.comment("Usikker på maaledatoen")

    
    
    #pp.pprint(json.loads(feature1.__repr__()))
    #print(json.loads(feature1.__repr__()))
    

    datafangst_collection = pnvdb.FeatureCollection()
    datafangst_collection.add_feature(feature1.feature())
    #print(datafangst_collection.push())
    pp.pprint(datafangst_collection.push())
    
    

