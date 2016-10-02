from pvdb import PvdbRead

r = PvdbRead()

data = r.get_status()


print(data)


