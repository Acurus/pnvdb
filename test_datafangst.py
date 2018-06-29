from pnvdb.var import auth
import pnvdb


if __name__ == '__main__':
    username = auth.username
    password = auth.password
    contractId = '7168c19c-e637-48fd-9771-61eb43c53d6f'
    datafangst = pnvdb.Datafangst(username, password, contractId)