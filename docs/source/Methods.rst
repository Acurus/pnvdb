Methods
=======

The following methods are avaliable in the Nvdb class in pnvdb.

initialize it as following::

    import pnvdb
    nvdb = pnvdb.Nvdb(client='Your-App-Name', contact='Your-contact-information')


status
------
Method for getting information about the current status of the API

`API endpoint status <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/status>`_

Code example::

   >>> status = nvdb.status()
   >>> print(status['datakatalog']['versjon'])
   2.10

objekt
------
Method for creating a spesific nvdb python :ref:`objekt`



`API endpoint vegobjekter <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekter>`_

Code example::

  >>> obj = nvdb.objekt(objekt_type=67, nvdb_id=89204552)
  >>> print(obj.metadata)
  {'versjon': 3, 'type': {'navn': 'Tunnelløp', 'id': 67}, 'startdato': '2014-01-17', 'sist_modifisert': '2017-10-23 15:15:50'}

Attributes
^^^^^^^^^^
* metadata - Dictionary
* geometri - Well known text
* foreldre - List of Objekt
* barn     - List of Objekt
* vegreferanser - List of Vegreferanse

Methods
^^^^^^^
* dump()

objekt_type
-----------
Method for creating a spesific nvdb python :ref:`objekt_type`

`API endpoint vegobjekttyper <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekttyper>`_

Code example::

   >>> obj = nvdb.objekt_type(objekt_type=67)
   >>> print(obj.metadata)
   {'objektliste_dato': '2012-05-08', 'sosinvdbnavn': 'Tunnelløp_67', 'sorteringsnummer': 5460, 'navn': 'Tunnelløp', 'kategorier': [], 'veiledning': '', 'stedfesting': 'LINJE', 'id': 67, 'beskrivelse': 'Utgravd eller utstøpt passasje gjennom jord/fjell eller under større lokk.  Har normalt inngang og utgang i dagen.  I spesielle tilfeller, f.eks når forgreninger eller kryss, kan det være utgang mot annet tunnelløp eller inngang fra annet tunnelløp. Se også Undergang, Skredoverbygg og Høydebegrensning.'}

Attributes
^^^^^^^^^^
* metadata - Dictionary
* relasjonstyper - Dictionary
* egenskapstyper List of dictionaries
* styringsparametere - Dictionary
* foreldre - List of Objekt
* barn     - List of Objekt

Methods
^^^^^^^
* dump() - returns the raw result form the API


vegreferanse
------------
Returns :ref:`vegreferanse` of specified location

`API endpoint veg <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/veg>`_

Code example::

   >>> vegref = nvdb.vegreferanse('1600Ev6hp12m1000')
   >>> print(vegref.geometri)
   POINT Z (270765 7038663 51.14699567634733)

Attributes
^^^^^^^^^^
detaljert - dictionary
veglenke - dictionary
geometri - Well known text


posisjon
--------
Returns a :ref:`posisjon` object

`API endpoint posisjon <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/posisjon>`_

Code example::

   >>> pos = nvdb.posisjon(x=269815,y=7038165)
   >>> print(pos.vegreferanse)
   1600 Rv706 hp52 m344

Attributes
^^^^^^^^^^
vegreferanse - :ref:`vegreferanse`

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

   >>> for fylke in nvdb.fylker():
   >>>     print(fylke.metadata['navn'])
   Østfold
   Akershus
   Oslo
   ...

Attributes
^^^^^^^^^^ 
* metadata    - Dictionary
* kartutsnitt - Dictionary
* senterpunkt - Dictionary
* objekt - :ref:`objekt`


objekt_typer
------------
Returns :ref:`objekt_type` of every avaliable obj type in nvdb

Code example::

   >>> objects = nvdb.objekt_typer()
   >>> print(objects[0].metadata)
   {'objektliste_dato': '2012-05-08', 'sosinvdbnavn': 'Skjerm_3', 'navn': 'Skjerm', 'id': 3, 'kategorier': [], 'stedfesting': 'LINJE', 'sorteringsnummer': 4760, 'veiledning': '', 'beskrivelse': 'En frittstående konstruksjon som skal være et hinder for f.eks støyutbredelse'}   


hent
----
Return a generator object that can be itterated over to fetch the results of the query.

`API endpoint vegobjekter <https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekter>`_


Code example::

   >>> area_filter = {'fylke':'2'} # Akershus
   >>> objekt_type = 581 # Tunnels
   >>> objects = nvdb.hent(objekt_type, area_filter)
   >>> for obj in objects:
   >>>        for egenskap in obj.egenskaper:
   >>>            if egenskap['id'] == 5225:
   >>>                print(egenskap['verdi'])
   Furusmotunnelen
   Blåkollen tunnel
   Hagantunnelen
   ...



