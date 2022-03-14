#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pytest
from mkad.wsgi.api import get_coordinates

@pytest.fixture
def address():
    return 'Svobody ulitsa, Molodezhnaya ulitsa'

def test_get_coordinates(address):
    matches = get_coordinates(address)
    assert len(matches) == 10