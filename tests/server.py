# pylint: disable=C1801

from eve_requests import Settings


def test_settings_defaults():
    settings = Settings()

    assert settings.base_url == "http://localhost:5000"
    assert settings.if_match is True
    assert settings.etag == "_etag"
    assert settings.status == "_status"
    assert settings.issues == "_issues"
    assert settings.items == "_items"
    assert settings.id_field == "_id"
    assert settings.created == "_created"
    assert settings.links == "_links"
