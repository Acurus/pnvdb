from pnvdb.var import auth
import pnvdb
import pprint
import json
import geojson

TEST_DATA = {
"type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [ [10.39241731, 63.43053048],
            [10.39495434, 63.43043698],
            [10.39579151, 63.42898665],
            [10.39272171, 63.42909269],
            [10.39241731, 63.43053048] ]
        ]
      },
      "properties": {
        "tag": "Forsterkningslag#1",
        "dataCatalogVersion": "2.06",
        "typeId": 227,
        "comment": "Usikker på måledatoen",
        "attributes": {
          "5543": "20160802"
         }
       }
    }
  ]
}



if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    username = auth.username
    password = auth.password
    contractId = '7168c19c-e637-48fd-9771-61eb43c53d6f'
    datafangst = pnvdb.Datafangst(username, password, contractId)
    poly = [[[10.39241731, 63.43053048],
            [10.39272171, 63.42909269],
            [10.39579151, 63.42898665],
            [10.39495434, 63.43043698],
            [10.39241731, 63.43053048],
            ]]

    feature1 = pnvdb.Feature(227,poly,"Forsterkningslag#1")
    feature1.attribute(5543,'20160802')
    feature1.comment("Fra Pnvdb")


    #print(feature1.feature())
    #print(type(feature1.feature()))
    #a = geojson.dumps(feature1.feature())
    #print(type(a))
    #print(a)
    

    datafangst_collection = pnvdb.FeatureCollection()
    datafangst_collection.add_feature(feature1.feature())
    print(datafangst_collection.push())
    #pp.pprint(TEST_DATA)
    #res = datafangst_collection.push()
    #print(type(res))
    #print(dir(res))
    #print(res.items())
    #pp.pprint(res)
    
    

