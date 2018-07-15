from pnvdb.var import auth
import pnvdb


if __name__ == '__main__':
    username = auth.username
    password = auth.password
    contractId = '7168c19c-e637-48fd-9771-61eb43c53d6f'
    datafangst = pnvdb.Datafangst(username, password, contractId)
    feature1 = pnvdb.Feature(96,(1,2),"test_objekt")
    feature1.attribute(985,'hei')

    feature2 = pnvdb.Feature(96,(2,5),"test_objekt1")
    feature2.attribute(985,'hadet')
    
    #print(feature1)

    datafangst_collection = pnvdb.FeatureCollection()
    datafangst_collection.add_feature(feature1)
    datafangst_collection.add_feature(feature2)
    print(datafangst_collection.push())
    
    

