from pvdb import PvdbRead
import json
import pandas as pd

r = PvdbRead()
cat = r.catalogue
for i in cat
    print(str(i)+'\n')


#with open('json_dumps\dump.json','w') as f:
#    f.write(str(ol))


'''
Sånn vil jeg bruke den: 

r = PvdbRead()
for entry in r.catalogue:
    print(entry.id)
    print(entry.name)
    print(entry.metadata)
'''