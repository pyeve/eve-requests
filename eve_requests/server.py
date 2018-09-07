class Settings:
    """
    Holds the settings of a remote Eve_ service which are relevant to a :class:`Client` instance.

    Basic Usage:

        >>> from eve_requests Client, Settings
        >>> settings = Settings('https://myapi.com/)
        >>> settings.if_match = False
        >>> settings.etag = "_my_custom_etag"
        >>> client = Client(settings)
    
    Initialize from a Swagger/OpenAPI documentation endpoint. 
    Needs Eve-Swagger_ to be active on the service (not implemented yet):

        >>> from eve_requests Client, Settings
        >>> settings = Settings.from_url("https://myapi.com/api-docs/settings.json")
        >>> client = Client(settings)
    
    Alternatively, and assuming you have it available, you can initialize directly 
    from the Eve settings file (not implemented yet):

        >>> from eve_requests Client, Settings
        >>> settings = Settings.from_file("settings.py")
        >>> client = Client(settings)
    
    .. _Eve:
       http://python-eve.org/
    
    .. _Eve-Swagger:
       http://github.com/pyeve/eve-swagger

    :param base_url: (optional) remote service entry point. 
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, base_url="http://localhost:5000"):
        """
        """
        #: Remote service base url or entry point (the home page).
        self.base_url = base_url

        #: Wether concurrency control is enabled on the service.
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

        #: Allows to customize the links field. Should match the remote ``LINKS``
        #: setting`. Defaults to ``_links``.
        self.links = "_links"

        self._meta_fields = [
            self.etag,
            self.created,
            self.updated,
            self.id_field,
            self.links,
        ]

    @property
    def meta_fields(self):
        """List of remote meta fields handled automatically by the service. """
        return self._meta_fields

    @staticmethod
    def from_url(url):
        """ Loads configuration from a remote OpenAPI (Swagger) endpoint and
        returns it as a new :class:`Settings` instance. 
        
        Note: 
            not implemented
        """
        raise NotImplementedError()

    @staticmethod
    def from_file(url):
        """ Loads configuration from standard Eve settings file and returns
        it as a new :class:`Settings` instance. 
        
        Note: 
            not implemented
        """
        raise NotImplementedError()
