# pylint: disable=C0330,W1401
from urllib.parse import urljoin
from requests import Request

import requests

from .server import Settings


class Client:
    """Allows to easily perform read and write operations against a remote
    RESTful web service which is powered by the Eve_ REST framework.

    This class wraps the Requests_ library, specifically the
    :class:`requests.Session` class which, amongst other features, leverages
    :obj:`urllib3`’s connection pooling. So if you’re making several requests to the
    same host, the underlying TCP connection will be reused, which can result
    in a significant performance increase.

    Basic Usage::

        >>> from eve_requests import Client, Settings
        >>> settings = Settings('https://myapi.com/)
        >>> client = Client(settings)
        >>> client.post('contacts', {"name": "john doe"}, auth=('user', 'pw'))
        <Response [201]>

    .. _Eve:
       http://python-eve.org/
    
    .. _Requests:
       http://python-requests.org/

    """

    def __init__(self, settings=None):
        #: Instance of :class:`requests.Session` used internally to perform
        #: HTTP requests.
        self.session = requests.Session()

        if settings:
            #: Remote service settings. Make sure these are properly set before
            #: invoking any of the read and write methods.
            #: Defaults to a new instance of :class:`Settings`.
            self.settings = settings
        else:
            self.settings = Settings()

    def post(self, url_or_endpoint, payload, **kwargs):
        """Sends a POST request.

        :param url_or_endpoint: Either a valid key from the
            :obj:`Settings.endpoints` dict, or the target URL.
        :param payload: JSON data to send as the body of the request.
        :param \*\*kwargs: Optional arguments that :obj:`requests.Request`
            takes.
        :returns: The :class:`requests.Response` object, which contains a 
            server’s response to an HTTP request.
        
        :raises ValueError: If :any:`settings` is not set.
        """
        req = self._build_post_request(url_or_endpoint, payload, **kwargs)
        return self._prepare_and_send_request(req)

    def put(self, url_or_endpoint, payload, unique_id=None, etag=None, **kwargs):
        """Sends a PUT request.

        :param url_or_endpoint: Either a valid key from the
            :obj:`Settings.endpoints` dict, or the target URL.
        :param payload: JSON data to send as the body of the request. If the
            JSON contains any :any:`Settings.meta_fields`, these will be
            stripped before the request is sent over to the remote service.
        :param unique_id: Optional id of the document being replaced on the
            remote service. If omitted, the id will be inferred from the
            payload.
        :param etag: Optional document ETag. If omitted, the ETag will be
            inferred from the payload.
        :param \*\*kwargs: Optional arguments that :obj:`requests.Request`
            takes.
        :returns: The :class:`requests.Response` object, which contains a 
            server’s response to an HTTP request.
        
        :raises ValueError: If the unique id is missing.
        :raises ValueError: If ETag is missing and :any:`Settings.if_match` is 
            enabled.
        :raises ValueError: If :any:`settings` is not set.
        """
        req = self._build_put_request(
            url_or_endpoint, payload, unique_id, etag, **kwargs
        )
        return self._prepare_and_send_request(req)

    def patch(self, url_or_endpoint, payload, unique_id=None, etag=None, **kwargs):
        """Sends a PATCH request.

        :param url_or_endpoint: Either a valid key from the
            :obj:`Settings.endpoints` dict, or the target URL.
        :param payload: JSON data to send as the body of the request. If the
            JSON contains any :any:`Settings.meta_fields`, these will be
            stripped before the request is sent over to the remote service.
        :param unique_id: Optional id of the document being updated on the
            remote service. If omitted, the id will be inferred from the
            payload.
        :param etag: Optional document ETag. If omitted, the ETag will be
            inferred from the payload.
        :param \*\*kwargs: Optional arguments that :obj:`requests.Request`
            takes.

        :returns: The :class:`requests.Response` object, which contains a 
            server’s response to an HTTP request.
        
        :raises ValueError: If the unique id is missing.
        :raises ValueError: If ETag is missing and :any:`Settings.if_match` is 
            enabled.
        :raises ValueError: If :any:`settings` is not set.
        """
        req = self._build_patch_request(
            url_or_endpoint, payload, unique_id, etag, **kwargs
        )
        return self._prepare_and_send_request(req)

    def delete(self, url_or_endpoint, etag, unique_id, payload=None, **kwargs):
        """Sends a DELETE request.

        :param url_or_endpoint: Either a valid key from the
            :obj:`Settings.endpoints` dict, or the target URL.
        :param unique_id: Optional id of the document being deleted on the
            remote service. If omitted, the id will be inferred from the
            payload.
        :param etag: Optional document ETag. If omitted, the ETag will be
            inferred from the payload.
        :param payload: Optional JSON data used to infer document id and ETag
            when they are not provided as arguments.
        :param \*\*kwargs: Optional arguments that :obj:`requests.Request`
            takes.

        :returns: The :class:`requests.Response` object, which contains a 
            server’s response to an HTTP request.
        
        :raises ValueError: If the unique id is missing.
        :raises ValueError: If ETag is missing and :any:`Settings.if_match`
            is enabled.
        :raises ValueError: If :any:`settings` is not set.
        """
        req = self._build_delete_request(
            url_or_endpoint, payload, etag, unique_id, **kwargs
        )
        return self._prepare_and_send_request(req)

    def get(self, url_or_endpoint, etag=None, unique_id=None, payload=None, **kwargs):
        """Sends a GET request.

        :param url_or_endpoint: Either a valid key from the
            :obj:`Settings.endpoints` dict, or the target URL.
        :param etag: Optional document ETag. If present, a `If-None-Match`
            header with the etag will be included with the request.
        :param unique_id: Optional id of the document being retrieved from the
            remote service. 
        :param payload: Optional JSON data used to infer document id and ETag
            when they are not provided as arguments. 
        :param \*\*kwargs: Optional arguments that :obj:`requests.Request`
            takes.

        :returns: The :class:`requests.Response` object, which contains a 
            server’s response to an HTTP request.
        
        :raises ValueError: If ETag is missing and :any:`Settings.if_match` is 
            enabled.
        :raises ValueError: If :any:`settings` is not set.
        """
        req = self._build_get_request(
            url_or_endpoint, etag, unique_id, payload, **kwargs
        )
        return self._prepare_and_send_request(req)

    def _build_post_request(self, url_or_endpoint, payload, **kwargs):
        self.__validate()
        url = self._resolve_url(url_or_endpoint)
        return Client.__build_request("POST", url, json=payload, **kwargs)

    def _build_put_request(
        self, url_or_endpoint, payload, unique_id=None, etag=None, **kwargs
    ):
        self.__validate()
        url = self._resolve_url(url_or_endpoint, payload, unique_id, id_required=True)
        headers = self._resolve_ifmatch_header(payload, etag)
        json = self._purge_meta_fields(payload)
        return Client.__build_request("PUT", url, json=json, headers=headers, **kwargs)

    def _build_patch_request(
        self, url_or_endpoint, payload, unique_id=None, etag=None, **kwargs
    ):
        self.__validate()
        url = self._resolve_url(url_or_endpoint, payload, unique_id, id_required=True)
        headers = self._resolve_ifmatch_header(payload, etag)
        json = self._purge_meta_fields(payload)
        return Client.__build_request(
            "PATCH", url, json=json, headers=headers, **kwargs
        )

    def _build_delete_request(
        self, url_or_endpoint, payload=None, unique_id=None, etag=None, **kwargs
    ):
        self.__validate()
        url = self._resolve_url(
            url_or_endpoint, payload=payload, unique_id=unique_id, id_required=True
        )
        headers = self._resolve_ifmatch_header(payload=payload, etag=etag)
        return Client.__build_request("DELETE", url, headers=headers, **kwargs)

    def _build_get_request(
        self, url_or_endpoint, etag=None, unique_id=None, payload=None, **kwargs
    ):
        self.__validate()
        url = self._resolve_url(url_or_endpoint, payload=payload, unique_id=unique_id)
        headers = self._resolve_if_none_match_header(etag=etag, payload=payload)
        return Client.__build_request("GET", url, headers=headers, **kwargs)

    def _resolve_url(
        self, url_or_endpoint, payload=None, unique_id=None, id_required=False
    ):
        if url_or_endpoint in self.settings.endpoints:
            endpoint = self.settings.endpoints[url_or_endpoint]
        else:
            endpoint = url_or_endpoint

        if unique_id:
            endpoint = "/".join([endpoint, unique_id])
        elif payload and self.settings.id_field in payload:
            endpoint = "/".join([endpoint, payload[self.settings.id_field]])
        else:
            if id_required:
                raise ValueError("Unique id is required")

        return urljoin(self.settings.base_url, endpoint)

    def _resolve_if_none_match_header(self, payload=None, etag=None):
        return_value = self._resolve_etag(payload, etag)
        return {"If-None-Match": return_value} if return_value else None

    def _resolve_ifmatch_header(self, payload=None, etag=None):
        return_value = self._resolve_etag(payload, etag)
        return {"If-Match": return_value} if return_value else None

    def _resolve_etag(self, payload=None, etag=None):
        if not self.settings.if_match:
            return None

        if etag:
            return etag
        if payload and self.settings.etag in payload:
            return payload[self.settings.etag]

        raise ValueError("ETag is required")

    def _purge_meta_fields(self, payload):
        return {
            key: value
            for (key, value) in payload.items()
            if key not in self.settings.meta_fields
        }

    def _prepare_and_send_request(self, request):
        request = self.session.prepare_request(request)
        return self.session.send(request)

    def __validate(self):
        if not self.settings:
            raise ValueError("Settings are required")

    @classmethod
    def __build_request(cls, method, url, json=None, headers=None, **kwargs):
        return Request(method, url, json=json, headers=headers, **kwargs)
