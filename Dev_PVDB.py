import pnvdb

nvdb = pnvdb.Nvdb(client='pnvdb', contact='jankyr@vegvesen.no')
#print(nvdb.status())
pos = nvdb.posisjon(x=269815,y=7038165)
print(pos.vegreferanse)
#print(nvdb.vegreferanse('1600Ev6hp12m1000'))
#
#for i in nvdb.regioner():
	#print(i.metadata)
	#print(i.objekt.metadata)
#
#for i in nvdb.fylker():
#	print(i.metadata)
#	print(i.objekt.metadata)
#
#for i in nvdb.vegavdelinger():
#	print(i.metadata)
#	print(i.objekt.metadata)
#
#for i in nvdb.kommuner():
#	print(i.metadata)
#	print(i.objekt.metadata)
#
#
#for i in nvdb.kontraktsomrader():
#	print(i.metadata)
#	print(i.objekt.metadata)
#
#for i in nvdb.riksvegruter():
#	print(i.metadata)
#	print(i.objekt.metadata)
#
#
#
#objekttyper = nvdb.objekt_typer()
#[print(i.metadata) for i in objekttyper]
#
#
#objekttype = nvdb.objekt_type(470)
#print(objekttype.metadata)
#print(objekttype.relasjonstyper)
#print(objekttype.styringsparametere)
#print(objekttype.egenskapstyper)
#for i in objekttype.foreldre:
#	print(i.metadata)
#print(objekttype.dump(format='xml'))
#
#
#objekt = nvdb.objekt(67,86543444)
#print(objekt.metadata)
#print(objekt.vegreferanser)
#print(objekt.egengeometri)
#print(objekt.geometri)
#print(objekt.barn)
#print(objekt.dump(format='xml'))
#
#omradefilter = {'fylke':'2'}
#objekter = nvdb.hent(581, omradefilter)
#for i in objekter:
#	for egenskap in i.egenskaper:
#		if egenskap['id'] == 5225:
#			print(egenskap['verdi'])
