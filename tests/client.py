# pylint: disable=W0212
from eve_requests import Client, Settings


def test_client_session_is_set_at_startup():
    client = Client()
    assert client.session is not None


def test_client_default_settings_are_set_at_startup():
    client = Client()
    assert isinstance(client.settings, Settings)
    assert client.settings.base_url == "http://localhost:5000"


def test_client_default_settings_can_be_overridden_at_startup():
    settings = Settings()
    settings.base_url = "mybase"
    client = Client(settings)
    assert client.settings.base_url == "mybase"


def test_resolve_url():
    client = Client()
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

    # urlib.parse.urljoin ignores non-absolute urls as base
    client.settings.base_url = "myapi"
    assert client._resolve_url("endpoint") == "endpoint"


def test_resolve_ifmatch_header():
    client = Client()

    assert client._resolve_ifmatch_header() is None
    assert client._resolve_ifmatch_header(None) is None
    assert client._resolve_ifmatch_header(None, None) is None

    headers = client._resolve_ifmatch_header({client.settings.etag: "hash"})
    assert headers["If-Match"] == "hash"

    assert client._resolve_ifmatch_header({"key": "value"}) is None

    headers = client._resolve_ifmatch_header(etag="etag")
    assert headers["If-Match"] == "etag"

    headers = client._resolve_ifmatch_header({client.settings.etag: "hash"}, "etag")
    assert headers["If-Match"] == "etag"

    client.settings.if_match = False
    assert client._resolve_ifmatch_header(None) is None
    assert client._resolve_ifmatch_header({client.settings.etag: "hash"}) is None
    assert client._resolve_ifmatch_header(etag="hash") is None
    assert (
        client._resolve_ifmatch_header({client.settings.etag: "hash"}, "etag") is None
    )


def test_purge_meta_fields():
    client = Client()
    payload = {meta_field: "value" for meta_field in client.settings.meta_fields}
    payload["key"] = "value"

    challenge = client._purge_meta_fields(payload)
    assert "key" in challenge
    for field in client.settings.meta_fields:
        assert field not in challenge

    # original has not been affected
    assert client.settings.meta_fields[0] in payload
