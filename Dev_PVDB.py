import pvdb
import json
import pandas as pd
from pprint import pprint

#nvdb = pvdb.Nvdb(client='pvdb', contact='jankyr@vegvesen.no')
#print(nvdb.status)
#test = nvdb.objekt(67,86543444)
#print(test.vegreferanser)
#print(test.egengeometri)
#print(test.geometri)
#print(test.barn)

def ja(fylke=0,region=0,vegreferanse=0):
	if fylke:
		print(fylke)
	if region:
		print(region)
	if vegreferanse:
		print(vegreferanse)
	return None
ja(vegreferanse=2)

