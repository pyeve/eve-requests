import collections

from eve_requests import Settings


def test_settings_defaults():
    settings = Settings()

    assert isinstance(settings.endpoints, collections.Mapping)
    assert len(settings.endpoints) == 0
    assert settings.base_url is None
    assert settings.if_match is True
    assert settings.etag == "_etag"
