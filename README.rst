Eve-Requests
============
Client SDK for Eve-powered RESTful APIs.

Usage
-----

.. code-block:: python

    settings = Settings()
    settings.base_url = "https://myapi"

    # or let the client auto-configure itself by downloading and
    # parsing the remote OpenAPI specification (will need Eve-Swagger
    # extension on the server). Currently raises NotImplemntedError.
    # settings = Settings.from_url('https://myapi/swagger.json')

    client = EveClient(settings)

    json = {"key1": "value1"}
    r = client.post("endpoint", json)

Current State
-------------
(very) early development. Feedback and contributors welcome.

License
-------
Eve-Requests is a `Nicola Iarocci`_ open source project,
distributed under the `BSD license
<https://github.com/pyeve/eve-requests/blob/master/LICENSE>`_.

.. _`Nicola Iarocci`: http://nicolaiarocci.com
.. _`funding page`: http://python-eve.org/funding