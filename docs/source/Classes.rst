
Classes
=======

Nvdb
----
The main class for interfacing with the API.

.. _objekt:

Objekt
------
Class for individual nvdb-objects. 

Attributes
^^^^^^^^^^
* metadata - Dictionary
* geometri - Well known text
* foreldre - List of Objekt
* barn     - List of Objekt
* vegreferanser - List of Vegreferanse

.. _objekt_type:

Objekt_type
-----------
Class for individual nvdb-object types. (Data catalogue)

Attributes
^^^^^^^^^^
* metadata - Dictionary
* relasjonstyper - Dictionary
* egenskapstyper List of dictionaries
* styringsparametere - Dictionary
* foreldre - List of Objekt
* barn     - List of Objekt

.. _vegreferanse:

Vegreferanse
------------
Class for working with road refferences.

Attributes
^^^^^^^^^^
detaljert - dictionary
veglenke - dictionary
geometri - Well known text

.. _posisjon:

Posisjon
--------
Class for connecting coordinates to road refferences
Vegreferanse

.. _area:

Area
----
Class for area objects.

Attributes
^^^^^^^^^^ 
* metadata    - Dictionary
* kartutsnitt - Dictionary
* senterpunkt - Dictionary
* objekt - Objekt