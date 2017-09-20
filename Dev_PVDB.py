import pvdb
import json
import pandas as pd
from pprint import pprint

nvdb = pvdb.Nvdb(client='pvdb', contact='jankyr@vegvesen.no')
print(nvdb.status)
test = nvdb.objekt(67,86543444)
#print(test.vegreferanser)
#print(test.egengeometri)
#print(test.geometri)

for barn in test.barn:
	try:
		print(barn.metadata['type']['navn'])
	except:
		pass



	
