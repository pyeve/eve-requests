class Settings:
    def __init__(self, base_url="http://localhost:5000"):
        self.endpoints = {}
        self.base_url = base_url
        self.if_match = True
        self.etag = "_etag"
        self.created = "_created"
        self.updated = "_updated"
        self.id_field = "_id"
        self.status = "_status"
        self.issues = "_issues"
        self.items = "_items"
        self.meta_fields = [self.etag, self.created, self.updated, self.id_field]

    @staticmethod
    def from_url(url):
        """ Loads configuration from a remote OpenAPI (Swagger) endpoint.
        """
        raise NotImplementedError()

    @staticmethod
    def from_file(url):
        """ Loads configuration from a Eve settings file.
        """
        raise NotImplementedError()
