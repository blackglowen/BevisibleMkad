#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pytest
from mkad.wsgi.api import spherical_distance

@pytest.fixture
def coordinates():
    return  [-97.441113, 35.221090, -97.520280, 35.465438]

# Determine the spherical distance (in km) between Oklahoma city
# at -97.441113 longitude, 35.221090 latitude and Norman at 
# -97.520280 longitude, 35.465438 latitude using Haversine formula.
# See https://en.wikipedia.org/wiki/Haversine_formula for more
# details.
#
# If sphercial_distance function returns 28.10308877116839, which 
# is the approximative known spherical distance between the two 
# cities, then the test passed.
def test_spherical_distance(coordinates):
    assert spherical_distance(coordinates) == 28.10308877116839