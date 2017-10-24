Methods
=======

The following methods are avaliable in the Nvdb class in pvdb.

initialize it as following::

    import pvdb
    nvdb = pvdb.Nvdb(client='Your-App-Name', contact='Your-contact-information')


status
------
Method for getting information about the current status of the API

`API endpoint status <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/status>`_

Code example::

   status = nvdb.status()
   print(status['datakatalog']['versjon'])

objekt
------
Method for creating a spesific nvdb python obj.

`API endpoint vegobjekter <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekter>`_

Code example::

   obj = nvdb.objekt(objekt_type=67, nvdb_id=89204552)

Attributes
^^^^^^^^^^
* metadata
* geometri
* foreldre
* barn
* vegreferanser

Methods
^^^^^^^
* dump()

objekt_type
-----------
Method for creating a spesific nvdb python obj type.

`API endpoint vegobjekttyper <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekttyper>`_

Code example::

   obj = nvdb.objekt(objekt_type=67)

Attributes
^^^^^^^^^^
* metadata
* relasjonstyper
* egenskapstyper
* styringsparametere
* foreldre
* barn

Methods
^^^^^^^
* dump()


vegreferanse
------------
Returns vegreferanse of specified lokation

`API endpoint veg <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/veg>`_

Code example::

   vegref = nvdb.vegreferanse('1600Ev6hp12m1000')
   print(vegref.geometri)

Attributes
^^^^^^^^^^
detaljert
veglenke
geometri



posisjon
--------
Returns a posisjons object

`API endpoint posisjon <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/posisjon>`_

Code example::

   pos = nvdb.posisjon(x=269815,y=7038165)
   print(pos.vegreferanse)

Attributes
^^^^^^^^^^
vegreferanse

areas
--------
Returns an Area object for different type of areas

`API endpoint omrader <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/omrader>`_

Avaliable areas : 
* regioner
* fylker
* vegavdelinger
* kommuner
* kontraktsomrader
* riksvegruter

Code example::
   for region in nvdb.regions():
     print(region.metadata)

Attributes
^^^^^^^^^^ 
* kartutsnitt
* senterpunkt
* objekt


objekt_typer
------------
Returns objekt_type of every avaliable obj type in nvdb

Code example::

   objects = nvdb.objekt_typer()
   for obj in objects:
      print(obj.metadata)

hent
----
Return objekt(s) based on search criteria

`API endpoint vegobjekter <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekter>`_

Code example::

   area_filter = {'fylke':'2'}
   objekt_type 581 # Tunnels
   objects = nvdb.hent(objekt_type, area_filter)
   for obj in objects:
      print(obj.metadata)





