from pnvdb.var import auth
import pnvdb


if __name__ == '__main__':
    username = auth.username
    password = auth.password
    contractId = '7168c19c-e637-48fd-9771-61eb43c53d6f'
    datafangst = pnvdb.Datafangst(username, password, contractId)
    datafangst_objekt = pnvdb.Df_Objekt(96,(1,2),"test_objekt")
    datafangst_objekt.attribute(985,'hei')
    print(datafangst_objekt)
    

