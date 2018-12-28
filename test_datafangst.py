from pnvdb.var import auth
import pnvdb
import pprint
import json
import geojson
import time

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    
    username = auth.username
    password = auth.password
    contractId = '7168c19c-e637-48fd-9771-61eb43c53d6f'
    
    datafangst = pnvdb.Datafangst(username, password, contractId)
    point = (10.39241731, 63.43053048)
    poly = [(10.39241731, 63.43053048),
            (10.39272171, 63.42909269),
            (10.39579151, 63.42898665),
            (10.39495434, 63.43043698),
            (10.39241731, 63.43053048),
            ]

    line = [(10.2, 63.4),
            (10.3, 63.4),
            (10.3, 63.5),
            ]
    
    feature1 = datafangst.feature(96, point, "Skilt")
    feature1.attribute(5530,8879)
    feature1.comment("Fra Pnvdb")

    feature2 = datafangst.feature(5, line, 'rekkverk')
    feature2.attribute(1089,13749)
    feature2.attribute(1248,4591)
    feature2.attribute(9591,13811)
    feature2.comment("Fra Pnvdb")

    feature3 = datafangst.feature(15, poly, 'Gras')
    feature3.attribute(4129,5092)
    feature3.comment("Fra Pnvdb")
    print(feature1.attribute)

    #datafangst_collection = datafangst.feature_collection()

    #datafangst_collection.add_feature(feature1)
    #datafangst_collection.add_feature(feature2)
    #datafangst_collection.add_feature(feature3)
    
    #pushed = datafangst_collection.push()
    #datafangst_collection.status()
    #time.sleep(3)
    #print(datafangst_collection.status())


