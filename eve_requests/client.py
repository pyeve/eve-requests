from urllib.parse import urljoin

import requests

from .server import Settings


class EveClient:
    def __init__(self, settings=None):
        self.session = requests.Session()

        if settings:
            self.settings = settings
        else:
            self.settings = Settings()

    def post(self, url_or_endpoint, json=None, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        # return self.session.post(url, json=json, **kwargs)

    def _resolve_url(self, url_or_endpoint):
        if url_or_endpoint in self.settings.endpoints:
            endpoint = self.settings.endpoints[url_or_endpoint]
        else:
            endpoint = url_or_endpoint
        return urljoin(self.settings.base_url, endpoint)

    def _resolve_ifmatch_header(self, json):
        if self.settings.if_match and self.settings.etag in json:
            return {"If-Match": json[self.settings.etag]}
        else:
            return None
