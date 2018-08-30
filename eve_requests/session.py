import requests


class Session(requests.Session):
    def __init__(self):
        self.endpoints = []
        self.base_url = None
        self.etag = "_etag"
        self.if_match = True
        super().__init__()

    def post(self, url_or_endpoint, json=None, **kwargs):
        if url_or_endpoint in self.endpoints:
            endpoint = self.endpoints[url_or_endpoint]
        else:
            endpoint = url_or_endpoint
        url = urljoin(self.config.base_url, endpoint)

        return super().post(url, json=json, **kwargs)
