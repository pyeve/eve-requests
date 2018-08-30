# pylint: disable=W0212
from eve_requests import EveClient, Settings


def test_client_session_is_set_at_startup():
    client = EveClient()
    assert client.session is not None


def test_client_default_settings_are_set_at_startup():
    client = EveClient()
    assert isinstance(client.settings, Settings)
    assert client.settings.base_url == "http://localhost:5000"


def test_client_default_settings_can_be_overridden_at_startup():
    settings = Settings()
    settings.base_url = "mybase"
    client = EveClient(settings)
    assert client.settings.base_url == "mybase"


def test_resolve_url():
    client = EveClient()
    assert client._resolve_url("endpoint") == "http://localhost:5000/endpoint"

    client.settings.base_url = "//myapi"
    assert client._resolve_url("endpoint") == "//myapi/endpoint"

    client.settings.base_url = "https://myapi"
    assert client._resolve_url("endpoint") == "https://myapi/endpoint"

    client.settings.endpoints["contacts"] = "people"
    assert client._resolve_url("contacts") == "https://myapi/people"

    assert client._resolve_url(None) == "https://myapi"

    client.settings.base_url = None
    assert client._resolve_url(None) is None

    # urlib.parse.urljoin ignores non-absolute url as base
    client.settings.base_url = "myapi"
    assert client._resolve_url("endpoint") == "endpoint"


def test_resolve_ifmatch_header():
    client = EveClient()
    assert client._resolve_ifmatch_header({"key": "value"}) is None

    headers = client._resolve_ifmatch_header({"key": "value", "_etag": "hash"})
    assert "If-Match" in headers
    assert headers["If-Match"] == "hash"

    client.settings.if_match = False
    assert client._resolve_ifmatch_header({"key": "value"}) is None
    assert client._resolve_ifmatch_header({"key": "value", "_etag": "hash"}) is None

    assert client._resolve_ifmatch_header(None) is None


def test_resolve_ifmatch_header_with_custom_etag():
    client = EveClient()
    client.settings.etag = "_custom_etag"

    assert client._resolve_ifmatch_header({"key": "value"}) is None
    assert client._resolve_ifmatch_header({"key": "value", "_etag": "hash"}) is None

    headers = client._resolve_ifmatch_header({"key": "value", "_custom_etag": "hash"})
    assert "If-Match" in headers
    assert headers["If-Match"] == "hash"
