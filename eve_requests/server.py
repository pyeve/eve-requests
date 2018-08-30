class Settings:
    def __init__(self):
        self.endpoints = {}
        self.base_url = "http://localhost:5000"
        self.if_match = True
        self.etag = "_etag"
        self.meta_fields = [self.etag]

    @staticmethod
    def from_url(url):
        """ TODO: download and parse OpenAI/Swagger specification,
        then return a Settings instance which has been initialized with 
        relevant settings from the server
         """
        raise NotImplementedError()
