from .server import Settings


def get_documents(json, settings=None):
    """Returns the documents contained within a JSON response. Standard server
    responses are quite information-rich; thus they contain serveral meta-fields:
    
        >>> r = client.get('people')
        <Response [201]>
        >>> r.json()
        {'_links': {...}, '_meta': {...}, '_items': [{'_id': '5b89b1b091a5d0000495f54e', 'lastname': 'Green', ...}]}

    While these are all useful, in many circumstances you are only interested in
    the actual documents returned by the server, and this is where this helper
    function comes in handy:

        >>> get_documents(r.json())
        [{'_id': '5b89b1b091a5d0000495f54e', 'lastname': 'Green', ...}]

    :param json: The dict that should be parsed. 
    :param settings: Optional :any:`Settings` instance to be used while
        processing ``json``. 

    :raises ValueError: If ``json`` does not contain a :any:`Settings.items` key.
    """
    if not settings:
        settings = Settings()

    if settings.items in json:
        return json[settings.items]

    raise ValueError("json does not contatin a '{0}' key".format(settings.items))


def purge_document(document, settings=None):
    """Returns a copy of a document, purged of all known meta fields.

        >>> r = client.get('people', unique_id="5b89b1b091a5d0000495f54e")
        <Response [200]>
        >>> r.json()
        {'_id': '5b89b1b091a5d0000495f54e', '_created': "....", _links': {...}, 'lastname': 'Green'}
        >>> purge_document(r.json())
        {'lastname': 'Green'}

    :param document: The original document.
    :param settings: Optional :any:`Settings` instance to be used while
        processing ``document``. 
    """
    if not settings:
        settings = Settings()

    return {
        key: value
        for (key, value) in document.items()
        if key not in settings.meta_fields
    }
