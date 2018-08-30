Eve-Requests
============
Client SDK for Eve-powered RESTful APIs.

Usage
-----

.. code-block:: python

    settings = Settings()
    settings.base_url = "https://eve-demo.herokuapp.com"

    # or let the settings auto-configure by downloading and parsing 
    # the remote OpenAPI specification (needs Eve-Swagger extension 
    # on the server). Currently raises NotImplemntedError.
    #
    # settings = Settings.from_url('https://myapi/docs/swagger.json')

    client = EveClient(settings)

    json = {"firstname": "john", "lastname": "doe"}
    r = client.post("people", json, auth=('user','pw'))

    # HTTP verbs return http://python-requests.org Request objects
    print(r.status_code)    # 201
    print(r.json())         # { ... }

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