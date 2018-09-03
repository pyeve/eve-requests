from urllib.parse import urljoin

import requests

from .server import ServerSettings


class Client:
    """Allows to easily perform read and write operations against a remote
    RESTful web service which is powered by the Eve_ REST framework.

    This class wraps the Requests_ library, specifically the
    :class:`requests.Session` class which, amongst other features, leverages
    :obj:`urllib3`’s connection pooling. So if you’re making several requests to the
    same host, the underlying TCP connection will be reused, which can result
    in a significant performance increase.

    Basic Usage::
        >>> from eve_requests import Client, ServerSettings
        >>> settings = ServerSettings('https://myapi.com/)
        >>> client = Client(settings)
        >>> client.post('people', {"name": "john doe"})
        <Response [201]>

    .. _Eve:
       http://python-eve.org/
    
    .. _Requests:
       http://python-requests.org/

    """

    def __init__(self, settings=None):
        # TODO: session should probably be public
        self._session = requests.Session()

        if settings:
            #: Remote server settings. Make sure these are properly set before
            #: invoking any of the read and write methods.
            #: Defaults to a new instance of :class:`ServerSettings`.
            self.server_settings = settings
        else:
            self.server_settings = ServerSettings()

    def post(self, url_or_endpoint, payload, **kwargs):
        url = self._resolve_url(url_or_endpoint)
        return self._session.post(url, json=payload, **kwargs)

    def put(self, url_or_endpoint, payload, unique_id=None, etag=None, **kwargs):
        url = self._resolve_url(url_or_endpoint, payload, unique_id)
        headers = self._resolve_ifmatch_header(payload, etag)
        json = self._purge_meta_fields(payload)
        return self._session.put(url, json=json, headers=headers, **kwargs)

    def patch(self, url_or_endpoint, payload, unique_id=None, etag=None, **kwargs):
        url = self._resolve_url(url_or_endpoint, payload, unique_id)
        headers = self._resolve_ifmatch_header(payload, etag)
        json = self._purge_meta_fields(payload)
        return self._session.patch(url, json=json, headers=headers, **kwargs)

    def delete(self, url_or_endpoint, etag, unique_id=None, **kwargs):
        url = self._resolve_url(url_or_endpoint, unique_id=unique_id)
        headers = self._resolve_ifmatch_header(etag=etag)
        return self._session.delete(url, headers=headers, **kwargs)

    def _resolve_url(self, url_or_endpoint, payload=None, unique_id=None):
        if url_or_endpoint in self.server_settings.endpoints:
            endpoint = self.server_settings.endpoints[url_or_endpoint]
        else:
            endpoint = url_or_endpoint
        if unique_id:
            endpoint = "/".join([endpoint, unique_id])
        elif payload and self.server_settings.id_field in payload:
            endpoint = "/".join([endpoint, payload[self.server_settings.id_field]])

        return urljoin(self.server_settings.base_url, endpoint)

    def _resolve_ifmatch_header(self, payload=None, etag=None):
        if not self.server_settings.if_match:
            return None

        if etag:
            return_value = etag
        elif payload:
            return_value = payload.get(self.server_settings.etag)
        else:
            return_value = None

        return {"If-Match": return_value} if return_value else None

    def _purge_meta_fields(self, payload):
        return {
            key: value
            for (key, value) in payload.items()
            if key not in self.server_settings.meta_fields
        }
