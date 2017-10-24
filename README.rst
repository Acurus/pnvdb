pvdb
====


pvdb stands for "python veg database" and is a python wrapper for the `NVDB Rest API <https://www.vegvesen.no/nvdb/apidokumentasjon/>`_


Data pulled from the API is licensed under
Norsk lisens for offentlige data `NLOD <http://data.norge.no/nlod/no/1.0>`_

Getting started
---------------

Read the docs at 
http://pvdb.readthedocs.io

Install
^^^^^^^^^^^^^^^::

	pip install pvdb

Quick Start
^^^^^^^^^^^

Start with initalizing an instance of pvdb::

    import pvdb
    nvdb = pvdb.Nvdb(client='Your-App-Name', contact='Your-contact-information')

Now we can test our connection to NVDB::

    print(nvdb.status())


To work with a spesific nvdb object, we can initialize it like this::

    objekt = nvdb.objekt(objekt_type=67, nvdb_id=86543444)
    

This will get us access to a number of attributes assosiated with this object. Let's print them out::

    print(objekt.metadata)
    print(objekt.vegreferanser)
    print(objekt.egengeometri)
    print(objekt.geometri)
    print(objekt.barn)

These are all dictionaries containing information to this spesific object.