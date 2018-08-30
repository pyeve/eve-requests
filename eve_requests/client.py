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
        return self.session.post(url, json=json, **kwargs)

    def put(self, url_or_endpoint, json=None, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        headers = self._resolve_ifmatch_header(json)
        json = self._purge_meta_fiels(json)
        return self.session.put(url, json=json, headers=headers, **kwargs)

    def patch(self, url_or_endpoint, json=None, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        headers = self._resolve_ifmatch_header(json)
        json = self._purge_meta_fiels(json)
        return self.session.patch(url, json=json, headers=headers, **kwargs)

    def delete(self, url_or_endpoint, etag, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        headers = self._resolve_ifmatch_header(etag)
        return self.session.delete(url, headers=headers, **kwargs)

    def _resolve_url(self, url_or_endpoint):
        if url_or_endpoint in self.settings.endpoints:
            endpoint = self.settings.endpoints[url_or_endpoint]
        else:
            endpoint = url_or_endpoint
        return urljoin(self.settings.base_url, endpoint)

    def _resolve_ifmatch_header(self, json_or_etag):
        if not self.settings.if_match:
            return None

        etag = None
        if isinstance(json_or_etag, str):
            etag = json_or_etag
        elif self.settings.etag in json_or_etag:
            etag = json_or_etag[self.settings.etag]
        return {"If-Match": etag} if etag else None

    def _purge_meta_fiels(self, json):
        for field in self.settings.meta_fields:
            try:
                del (json[field])
            except ValueError:
                pass
        return json
