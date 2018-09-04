class Settings:
    """
    Holds the settings of a remote Eve_ service which are relevant to a :class:`Client` instance.

    Basic Usage::
        >>> from eve_requests Client, Settings
        >>> settings = Settings('https://myapi.com/)
        >>> settings.if_match = False
        >>> settings.etag = "_my_custom_etag"
        >>> client = Client(settings)

    .. _Eve:
       http://python-eve.org/
    
    :param base_url: (optional) remote service entry point. 
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, base_url="http://localhost:5000"):
        """
        """
        #: A :obj:`dict` mapping endpoints to actual urls.
        #: Example: ``{"contacts": "people"}`` would map the contacts endpoint to the people url.
        #: Defaults to ``{}``.
        self.endpoints = {}

        #: Remote service base url or entry point (the home page).
        self.base_url = base_url

        #: Wether `concurrency control <http://python-eve.org/features.html#data-integrity-and-concurrency-control>`_ is enabled on the service.
        #: Should match the remote ``IF_MATCH`` setting. Defaults to
        #:``True``.
        self.if_match = True

        #: Allows to customize the etag field. Should match the remote
        #: ``ETAG`` setting. Defaults to ``_etag``.
        self.etag = "_etag"

        #: Name for the field used to record a document creation date. Should
        #: match the remote ``DATE_CREATED`` setting. Defaults to ``_created``.
        self.created = "_created"

        #: Name for the field used to record a document's last update date.
        #: Should match the remote ``DATE_UPDATED`` setting. Defaults to
        #: ``_updated``.
        self.updated = "_updated"

        #: Name of the field used to uniquely identify remote documents. Should match
        #: the remote ``FIELD_ID`` setting. Defaults to ``_id``.
        self.id_field = "_id"

        #: Allows to customize the status field. Should match the remote ``STATUS``
        #: setting. Defaults to ``_status``.
        self.status = "_status"

        #: Allows to customize the issues field. Should match the remote ``ISSUES``
        #: setting. Defaults to ``_issues``.
        self.issues = "_issues"

        #: Allows to customize the items field. Should match the remote ``ITEMS``
        #: setting. Defaults to ``_items``.
        self.items = "_items"

        self._meta_fields = [self.etag, self.created, self.updated, self.id_field]

    @property
    def meta_fields(self):
        """List of remote meta fields handled automatically by the service. """
        return self._meta_fields

    @staticmethod
    def from_url(url):
        """ Loads configuration from a remote OpenAPI (Swagger) endpoint and
        returns it as a new :class:`Settings` instance. """
        raise NotImplementedError()

    @staticmethod
    def from_file(url):
        """ Loads configuration from standard Eve settings file and returns
        it as a new :class:`Settings` instance. """
        raise NotImplementedError()
