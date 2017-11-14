import pnvdb

nvdb = pnvdb.Nvdb(client='pnvdb', contact='jankyr@vegvesen.no')
#print(nvdb.status())
# pos = nvdb.posisjon(x_coordinate=269815,y_coordinate=7038165)
# print(pos.vegreferanse)
# vegref = nvdb.vegreferanse('1600Ev6hp12m1000')
# print(vegref)
# print(vegref.detaljert)
# print(vegref.veglenke)
# print(vegref.geometri)

# for i in nvdb.regioner():
#     print(i.metadata)
#     print(i.objekt.metadata)
#     break

# for i in nvdb.fylker():
#     print(i.metadata)
#     print(i.objekt.metadata)
#     break

# for i in nvdb.vegavdelinger():
#     print(i.metadata)
#     print(i.objekt.metadata)
#     break

# for i in nvdb.kommuner():
#     print(i.metadata)
#     print(i.objekt.metadata)
#     break

# for i in nvdb.kontraktsomrader():
#     print(i.metadata)
#     print(i.objekt.metadata)
#     break

# for i in nvdb.riksvegruter():
#     print(i.metadata)
#     print(i.objekt.metadata)
#     break



# objekttyper = nvdb.objekt_typer()
# [print(i.metadata) for i in objekttyper]


# objekttype = nvdb.objekt_type(470)
# print(objekttype.metadata)
# print(objekttype.relasjonstyper)
# print(objekttype.styringsparametere)
# print(objekttype.egenskapstyper)
# print(objekttype.egenskapstype(3779))
# for i in objekttype.foreldre:
#     print(i.metadata)
#     break
# print(objekttype.dump(file_format='xml'))


# objekt = nvdb.objekt(67,86543444)
# print(objekt.egenskap(1081)['verdi'])  #Navn
# print(objekt.egenskap(1083))  #Finnes ikke
# print(objekt.metadata.keys())
# print(objekt.egenskaper[0].keys())
# print(objekt.vegreferanser)
# print(objekt.egengeometri)
# print(objekt.geometri)
# print(objekt.barn)
# print(objekt.dump(file_format='xml'))

# omradefilter = {'fylke':'2'}
# objekter = nvdb.hent(581, omradefilter)
# for i in objekter:
#     for egenskap in i.egenskaper:
#         if egenskap['id'] == 5225:
#             print(egenskap['verdi'])
#             break
#     break

# criteria = {'fylke':'2','egenskap':'1820>=20'} # 1820 = "Takst liten bil"
criteria = {'kommune':'0828','egenskap':'1820>=20'} # Should return no result

obj = nvdb.hent(45, criteria)
print(obj)

"""
for i in obj:
    for egenskap in i.egenskaper:
        if egenskap['id'] == 1078:  # 1078 = "Navn bomstasjon"
            #print(egenskap['verdi'])
            break
    break
"""