import pvdb
import json
import pandas as pd
from pprint import pprint

nvdb = pvdb.Nvdb(client='pvdb', contact='jankyr@vegvesen.no')
#print(nvdb.status)

#objekttyper = nvdb.objekt_typer()
#[print(i.metadata) for i in objekttyper]


#objekttype = nvdb.objekt_type(105)
#print(objekttype.metadata)
#print(objekttype.relasjonstyper)
#print(objekttype.styringsparametere)
#print(objekttype.egenskapstyper)

#objekt = nvdb.objekt(67,86543444)
#print(objekt.metadata)
#print(objekt.vegreferanser)
#print(objekt.egengeometri)
#print(objekt.geometri)
#print(objekt.barn)

objekter = nvdb.hent(105, {'kommune':'1601'})
for i in objekter:
	print(i.metadata)

