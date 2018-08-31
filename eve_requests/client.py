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

    def post(self, url_or_endpoint, payload, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        return self.session.post(url, json=payload, **kwargs)

    def put(self, url_or_endpoint, payload, etag=None, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        headers = self._resolve_ifmatch_header(payload, etag)
        json = self._purge_meta_fields(payload)
        return self.session.put(url, json=json, headers=headers, **kwargs)

    def patch(self, url_or_endpoint, payload, etag=None, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        headers = self._resolve_ifmatch_header(payload, etag)
        json = self._purge_meta_fields(payload)
        return self.session.patch(url, json=json, headers=headers, **kwargs)

    def delete(self, url_or_endpoint, etag, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        headers = self._resolve_ifmatch_header(etag=etag)
        return self.session.delete(url, headers=headers, **kwargs)

    def _resolve_url(self, url_or_endpoint):
        if url_or_endpoint in self.settings.endpoints:
            endpoint = self.settings.endpoints[url_or_endpoint]
        else:
            endpoint = url_or_endpoint
        return urljoin(self.settings.base_url, endpoint)

    def _resolve_ifmatch_header(self, payload=None, etag=None):
        if not self.settings.if_match:
            return None

        if etag:
            return_value = etag
        elif payload:
            return_value = payload.get(self.settings.etag)
        else:
            return_value = None

        return {"If-Match": return_value} if return_value else None

    def _purge_meta_fields(self, payload):
        return {
            key: value
            for (key, value) in payload.items()
            if key not in self.settings.meta_fields
        }
