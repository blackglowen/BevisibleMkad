#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pytest
from mkad.wsgi.api import is_invalid_address

@pytest.fixture
def addr():
    return 'Some Invalid Address $TF+ffdf'

# Simple unit test to check whether the string representing an address 
# returns by the fixture addr is invalid or not
def test_is_invalid_address(addr):
    assert is_invalid_address(addr) == True
