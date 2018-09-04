# pylint: disable=W0212
import pytest

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

    assert (
        client._resolve_url("endpoint", unique_id="id") == "https://myapi/endpoint/id"
    )

    # unique_id takes precedence over the payload
    assert (
        client._resolve_url(
            "endpoint", {client.settings.id_field: "payload_id"}, "id"
        )
        == "https://myapi/endpoint/id"
    )

    client.settings.endpoints["contacts"] = "people"
    assert client._resolve_url("contacts") == "https://myapi/people"

    assert client._resolve_url(None) == "https://myapi"

    assert (
        client._resolve_url("contacts", {client.settings.id_field: "id"})
        == "https://myapi/people/id"
    )
    assert client._resolve_url("contacts", {"key": "value"}) == "https://myapi/people"

    client.settings.base_url = None
    assert client._resolve_url(None) is None

    # urlib.parse.urljoin ignores non-absolute urls as base
    client.settings.base_url = "myapi"
    assert client._resolve_url("endpoint") == "endpoint"


def test_resolve_ifmatch_header():
    client = Client()

    with pytest.raises(ValueError, message="ETag is required"):
        client._resolve_ifmatch_header()
        client._resolve_ifmatch_header(None)
        client._resolve_ifmatch_header(None, None)
        assert client._resolve_ifmatch_header({"key": "value"}) is None

    headers = client._resolve_ifmatch_header({client.settings.etag: "hash"})
    assert headers["If-Match"] == "hash"

    headers = client._resolve_ifmatch_header(etag="etag")
    assert headers["If-Match"] == "etag"

    headers = client._resolve_ifmatch_header(
        {client.settings.etag: "hash"}, "etag"
    )
    assert headers["If-Match"] == "etag"

    client.settings.if_match = False
    assert client._resolve_ifmatch_header() is None
    assert client._resolve_ifmatch_header(None) is None
    assert client._resolve_ifmatch_header(None, None) is None
    assert client._resolve_ifmatch_header({client.settings.etag: "hash"}) is None
    assert client._resolve_ifmatch_header(etag="hash") is None
    assert (
        client._resolve_ifmatch_header({client.settings.etag: "hash"}, "etag")
        is None
    )


def test_resolve_if_none_match_header():
    client = Client()

    with pytest.raises(ValueError, message="ETag is required"):
        assert client._resolve_if_none_match_header()
        assert client._resolve_if_none_match_header(None)
        assert client._resolve_if_none_match_header(None, None)

    headers = client._resolve_if_none_match_header(
        {client.settings.etag: "hash"}
    )
    assert headers["If-None-Match"] == "hash"

    headers = client._resolve_if_none_match_header(etag="etag")
    assert headers["If-None-Match"] == "etag"

    headers = client._resolve_if_none_match_header(
        {client.settings.etag: "hash"}, "etag"
    )
    assert headers["If-None-Match"] == "etag"

    client.settings.if_match = False
    assert client._resolve_if_none_match_header() is None
    assert client._resolve_if_none_match_header(None) is None
    assert client._resolve_if_none_match_header(None, None) is None
    assert (
        client._resolve_if_none_match_header({client.settings.etag: "hash"})
        is None
    )
    assert client._resolve_if_none_match_header(etag="hash") is None
    assert (
        client._resolve_if_none_match_header(
            {client.settings.etag: "hash"}, "etag"
        )
        is None
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


def test_post_method():
    client = Client()
    client.settings.endpoints["test"] = "people"
    req = client._build_post_request("test", {"key": "value"}, auth={"user", "pw"})
    assert req.url == "http://localhost:5000/people"
    assert req.json["key"] == "value"
    assert req.auth == set(["user", "pw"])

    req = client._build_post_request("foo", {"key": "value"})
    assert req.url == "http://localhost:5000/foo"
    assert req.json["key"] == "value"
    assert not req.auth


def test_put_method():
    client = Client()
    client.settings.endpoints["test"] = "people"
    req = client._build_put_request(
        "test",
        {
            client.settings.id_field: "id",
            client.settings.etag: "etag",
            "key": "value",
        },
        auth={"user", "pw"},
    )
    assert req.url == "http://localhost:5000/people/id"
    assert req.json["key"] == "value"
    assert req.headers["If-Match"] == "etag"
    assert req.auth == set(["user", "pw"])

    req = client._build_put_request(
        "foo", {"key": "value"}, unique_id="foo_id", etag="foo_etag"
    )
    assert req.url == "http://localhost:5000/foo/foo_id"
    assert req.json["key"] == "value"
    assert req.headers["If-Match"] == "foo_etag"
    assert not req.auth

    with pytest.raises(ValueError, message="ETag is required"):
        client._build_put_request("foo", {"key": "value"}, unique_id="id")

    with pytest.raises(ValueError, message="Unique id is required"):
        client._build_put_request("foo", {"key": "value"})


def test_patch_method():
    client = Client()
    client.settings.endpoints["test"] = "people"
    req = client._build_patch_request(
        "test",
        {
            client.settings.id_field: "id",
            client.settings.etag: "etag",
            "key": "value",
        },
        auth={"user", "pw"},
    )
    assert req.url == "http://localhost:5000/people/id"
    assert req.json["key"] == "value"
    assert req.headers["If-Match"] == "etag"
    assert req.auth == set(["user", "pw"])

    req = client._build_patch_request(
        "foo", {"key": "value"}, unique_id="foo_id", etag="foo_etag"
    )
    assert req.url == "http://localhost:5000/foo/foo_id"
    assert req.json["key"] == "value"
    assert req.headers["If-Match"] == "foo_etag"
    assert not req.auth

    with pytest.raises(ValueError, message="ETag is required"):
        client._build_put_request("foo", {"key": "value"}, unique_id="id")

    with pytest.raises(ValueError, message="Unique id is required"):
        client._build_patch_request("foo", {"key": "value"})


def test_delete_method():
    client = Client()
    client.settings.endpoints["test"] = "people"
    req = client._build_delete_request("test", None, "id", "etag", auth={"user", "pw"})
    assert req.url == "http://localhost:5000/people/id"
    assert req.headers["If-Match"] == "etag"
    assert req.auth == set(["user", "pw"])

    req = client._build_delete_request(
        "test", {client.settings.etag: "etag"}, "id", auth={"user", "pw"}
    )
    assert req.url == "http://localhost:5000/people/id"
    assert req.headers["If-Match"] == "etag"
    assert req.auth == set(["user", "pw"])

    req = client._build_delete_request(
        "test",
        {client.settings.etag: "etag", client.settings.id_field: "id"},
        auth={"user", "pw"},
    )
    assert req.url == "http://localhost:5000/people/id"
    assert req.headers["If-Match"] == "etag"
    assert req.auth == set(["user", "pw"])

    with pytest.raises(ValueError, message="ETag is required"):
        client._build_delete_request("foo", None, None)

    with pytest.raises(ValueError, message="ETag is required"):
        client._build_delete_request("foo", None, "id")

    with pytest.raises(ValueError, message="ETag is required"):
        client._build_delete_request("foo", {"key": "value"}, "id")

    with pytest.raises(ValueError, message="Unique id is required"):
        client._build_delete_request("foo", None, None, "etag")

    with pytest.raises(ValueError, message="Unique id is required"):
        client._build_delete_request("foo", {client.settings.etag: "etag"})


def test_get_method():
    client = Client()
    client.settings.endpoints["test"] = "people"
    req = client._build_get_request(
        "test", etag="etag", unique_id="id", auth=("user", "pw")
    )
    assert req.url == "http://localhost:5000/people/id"
    assert req.headers["If-None-Match"] == "etag"
    assert req.auth == tuple(["user", "pw"])

    with pytest.raises(ValueError, message="ETag is required"):
        req = client._build_get_request("foo")

    client.settings.if_match = False
    req = client._build_get_request("foo")
    assert req.url == "http://localhost:5000/foo"
    assert "If-None-Match" not in req.headers
    assert not req.auth
