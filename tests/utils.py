import pytest
from eve_requests.utils import purge_document, get_documents
from eve_requests.server import Settings


def test_purge_standard_meta_fields():
    settings = Settings()
    payload = {meta_field: "value" for meta_field in settings.meta_fields}
    payload["key"] = "value"

    challenge = purge_document(payload)
    assert "key" in challenge
    for field in settings.meta_fields:
        assert field not in challenge

    # original has not been affected
    assert settings.meta_fields[0] in payload


def test_purge_custom_meta_fields():
    settings = Settings()
    settings.created = "_one"
    settings.updated = "_two"
    payload = {meta_field: "value" for meta_field in settings.meta_fields}
    payload["key"] = "value"

    challenge = purge_document(payload, settings=settings)
    assert "key" in challenge
    for field in settings.meta_fields:
        assert field not in challenge

    # original has not been affected
    assert settings.created in payload
    assert settings.updated in payload


def test_get_documents():
    settings = Settings()
    json = {settings.items: ["doc1", "doc2"]}
    challenge = get_documents(json)

    assert "doc1" in challenge
    assert "doc2" in challenge

    settings.items = "_foo"
    with pytest.raises(
        ValueError, message="json does not contain a '{}' key".format(settings.items)
    ):
        challenge = get_documents(json, settings)
