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
    
    feature1 = datafangst.feature(227, line, "Forsterkningslag#1")
    feature1.attribute(5543,'20160802')
    feature1.comment("Fra Pnvdb")


    datafangst_collection = datafangst.feature_collection()
    datafangst_collection.add_feature(feature1.feature())
    pushed = datafangst_collection.push()


