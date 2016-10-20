import pvdb
import json
import pandas as pd
from pprint import pprint

r = pvdb.Read()
cat = pvdb.Catalogue()
objects = cat.objects('')
pprint(r.status)

for obj in objects:
    print('ID: {}\t{}'.format(obj['id'], obj['navn']))

obj = cat.object('25', '')

print(obj.keys())
print(obj['egenskapstyper'][2].keys())
