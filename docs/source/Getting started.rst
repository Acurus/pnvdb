Getting started
===============

code::

    import pvdb

    nvdb = pvdb.Nvdb(client='pvdb', contact='jankyr@vegvesen.no')
	print(nvdb.status())
    objekt = nvdb.objekt(67,86543444)
	print(objekt.metadata)
	print(objekt.vegreferanser)
	print(objekt.egengeometri)
	print(objekt.geometri)
	print(objekt.barn)



