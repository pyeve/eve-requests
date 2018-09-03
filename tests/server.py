# pylint: disable=C1801

import collections

from eve_requests import ServerSettings


def test_settings_defaults():
    settings = ServerSettings()

    assert isinstance(settings.endpoints, collections.Mapping)
    assert len(settings.endpoints) == 0
    assert settings.base_url == "http://localhost:5000"
    assert settings.if_match is True
    assert settings.etag == "_etag"
    assert settings.status == "_status"
    assert settings.issues == "_issues"
    assert settings.items == "_items"
    assert settings.id_field == "_id"
