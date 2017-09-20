import pvdb
import json
import pandas as pd
from pprint import pprint

nvdb = pvdb.Nvdb(client='pvdb', contact='jankyr@vegvesen.no')
print(nvdb.status)
lop = nvdb.object(67,89204552)
for att in lop.attributes:
	print(att['navn'])

print(lop.metadata)
print(lop.geometry)
print(lop.relations)
	
