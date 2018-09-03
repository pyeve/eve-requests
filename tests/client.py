# pylint: disable=W0212
from eve_requests import Client, ServerSettings


def test_client_session_is_set_at_startup():
    client = Client()
    assert client._session is not None


def test_client_default_settings_are_set_at_startup():
    client = Client()
    assert isinstance(client.server_settings, ServerSettings)
    assert client.server_settings.base_url == "http://localhost:5000"


def test_client_default_settings_can_be_overridden_at_startup():
    settings = ServerSettings()
    settings.base_url = "mybase"
    client = Client(settings)
    assert client.server_settings.base_url == "mybase"


def test_resolve_url():
    client = Client()
    assert client._resolve_url("endpoint") == "http://localhost:5000/endpoint"

    client.server_settings.base_url = "//myapi"
    assert client._resolve_url("endpoint") == "//myapi/endpoint"

    client.server_settings.base_url = "https://myapi"
    assert client._resolve_url("endpoint") == "https://myapi/endpoint"

    assert (
        client._resolve_url("endpoint", unique_id="id") == "https://myapi/endpoint/id"
    )

    # unique_id takes precedence over the payload
    assert (
        client._resolve_url(
            "endpoint", {client.server_settings.id_field: "payload_id"}, "id"
        )
        == "https://myapi/endpoint/id"
    )

    client.server_settings.endpoints["contacts"] = "people"
    assert client._resolve_url("contacts") == "https://myapi/people"

    assert client._resolve_url(None) == "https://myapi"

    assert (
        client._resolve_url("contacts", {client.server_settings.id_field: "id"})
        == "https://myapi/people/id"
    )
    assert client._resolve_url("contacts", {"key": "value"}) == "https://myapi/people"

    client.server_settings.base_url = None
    assert client._resolve_url(None) is None

    # urlib.parse.urljoin ignores non-absolute urls as base
    client.server_settings.base_url = "myapi"
    assert client._resolve_url("endpoint") == "endpoint"


def test_resolve_ifmatch_header():
    client = Client()

    assert client._resolve_ifmatch_header() is None
    assert client._resolve_ifmatch_header(None) is None
    assert client._resolve_ifmatch_header(None, None) is None

    headers = client._resolve_ifmatch_header({client.server_settings.etag: "hash"})
    assert headers["If-Match"] == "hash"

    assert client._resolve_ifmatch_header({"key": "value"}) is None

    headers = client._resolve_ifmatch_header(etag="etag")
    assert headers["If-Match"] == "etag"

    headers = client._resolve_ifmatch_header(
        {client.server_settings.etag: "hash"}, "etag"
    )
    assert headers["If-Match"] == "etag"

    client.server_settings.if_match = False
    assert client._resolve_ifmatch_header(None) is None
    assert client._resolve_ifmatch_header({client.server_settings.etag: "hash"}) is None
    assert client._resolve_ifmatch_header(etag="hash") is None
    assert (
        client._resolve_ifmatch_header({client.server_settings.etag: "hash"}, "etag")
        is None
    )


def test_resolve_if_none_match_header():
    client = Client()

    assert client._resolve_if_none_match_header() is None
    assert client._resolve_if_none_match_header(None) is None
    assert client._resolve_if_none_match_header(None, None) is None

    headers = client._resolve_if_none_match_header(
        {client.server_settings.etag: "hash"}
    )
    assert headers["If-None-Match"] == "hash"

    assert client._resolve_if_none_match_header({"key": "value"}) is None

    headers = client._resolve_if_none_match_header(etag="etag")
    assert headers["If-None-Match"] == "etag"

    headers = client._resolve_if_none_match_header(
        {client.server_settings.etag: "hash"}, "etag"
    )
    assert headers["If-None-Match"] == "etag"

    client.server_settings.if_match = False
    assert client._resolve_if_none_match_header(None) is None
    assert (
        client._resolve_if_none_match_header({client.server_settings.etag: "hash"})
        is None
    )
    assert client._resolve_if_none_match_header(etag="hash") is None
    assert (
        client._resolve_if_none_match_header(
            {client.server_settings.etag: "hash"}, "etag"
        )
        is None
    )


def test_purge_meta_fields():
    client = Client()
    payload = {meta_field: "value" for meta_field in client.server_settings.meta_fields}
    payload["key"] = "value"

    challenge = client._purge_meta_fields(payload)
    assert "key" in challenge
    for field in client.server_settings.meta_fields:
        assert field not in challenge

    # original has not been affected
    assert client.server_settings.meta_fields[0] in payload
