#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pytest

from mkad.wsgi import make_app


@pytest.fixture
def client():
    app = make_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_find_matched_addresses(client):
    url = '/mkad/api/Svobody ulitsa, Molodezhnaya ulitsa'
    response = client.get(url, follow_redirects=True)
    assert b'Svobody ulitsa' in response.data