import pnvdb

nvdb = pnvdb.Nvdb(client='pnvdb', contact='jankyr@vegvesen.no')

params = {'fylke':'2','egenskap':'1820>=20'}
bomstasjoner = nvdb.hent(45,params)
for bomstasjon in bomstasjoner:
	print(bomstasjon.metadata)
