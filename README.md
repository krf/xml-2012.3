XML-Technologien (Gruppe III)
=============================

Members
-------

* Kevin Funk
* Jan Kustolski
* André Zoufahl
* Konrad Reiche
* David Bialik

Dependencies
------------

* BaseX (http://basex.org/)
* Python LXML (http://lxml.de)
* SPARQL Endpoint interface to Python (http://sparql-wrapper.sourceforge.net/)
* Python CJSON (http://pypi.python.org/pypi/python-cjson)

Quick install (Ubuntu):
* apt-get install basex python-lxml python-cjson python-sparqlwrapper

Running
-----

Prerequisites:
* $ export PYTHONPATH=./src

Run basexserver (should contain data)
*  $ basexserver

Run web server:
*  $ cd src/
*  $ ./web/web.py

This starts a web server on http://localhost:8888
