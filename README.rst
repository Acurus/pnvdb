pnvdb
====


pnvdb stands for "python for Nasjonal vegdatabank" and is a python wrapper for the `NVDB Rest API <https://www.vegvesen.no/nvdb/apidokumentasjon/>`_


Data pulled from the API is licensed under
Norsk lisens for offentlige data `NLOD <http://data.norge.no/nlod/no/1.0>`_

Getting started
---------------

Read the docs at 
http://pnvdb.readthedocs.io

Install
^^^^^^^
::

	pip install pnvdb


Quick Start
^^^^^^^^^^^

Start with initalizing an instance of pnvdb::

    >>> import pnvdb
    >>> nvdb = pnvdb.Nvdb(client='Your-App-Name', contact='Your-contact-information')

Now we can test our connection to NVDB::

    >>> print(nvdb.status())
    {'datagrunnlag': {'sist_oppdatert': '2017-11-05 11:59:37'}, 'datakatalog': {'id': 782, 'dato': '2017-09-29', 'versjon': '2.10'}}


To work with a spesific nvdb object, we can initialize it like this::

    >>> objekt = nvdb.objekt(objekt_type=67, nvdb_id=86543444)
    

This will get us access to a number of attributes assosiated with this object. Let's print one out::

    >>> print(objekt.metadata)
    {'type': {'id': 67, 'navn': 'Tunnelløp'}, 'versjon': 14, 'startdato': '2014-09-19', 'sist_modifisert': '2017-10-24 15:40:48'}
    
