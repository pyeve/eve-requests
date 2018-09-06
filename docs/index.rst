.. Eve-Requests documentation master file, created by
   sphinx-quickstart on Fri Aug 31 11:55:47 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Eve-Requests
========================

Eve-Requests is a Python client for RESTful web services built with the
Eve_ framework. It knows all about Eve features and transparently leverages
them to make your coding experience as pleasant and seamless as possible.

The client itself is but a tiny wrapper around the beautiful Requests_
library. If you know Requests, you also know Eve-Requests.

Quickstart
----------
An example is worth a thousand words. Let's assume we have a REST service up
and running at https://eve-demo.herokuapp.com. We want to perform some CRUD
operations against it.

First, we need to initialise our client:

    >>> from eve_requests import Client, Settings
    >>> settings = Settings('https://eve-demo.herokuapp.com/')
    >>> client = Client(settings)

As you guessed, ``settings`` holds server configuration options relevant to
the client. Its attributes default to Eve defaults, so most of the time you
can get away with only updating the base URL (which defaults to
http://localhost:5000). For a rundown on available settings, see the
:class:`eve_requests.Settings` class.

Now that the client is ready let's download the documents available at the
*people* endpoint: 

    >>> r = client.get('people', auth=('user', 'pw'))
    >>> r.status_code
    200
    >>> r.json()
    {'_items': [{'_id': '5b89b1b091a5d0000495f54e', 'lastname': 'Green', ... }
    
.. _Eve:
    http://python-eve.org/

.. _Requests:
    http://python-requests.org/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
