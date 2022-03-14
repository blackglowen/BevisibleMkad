#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
from typing import List

EARTH_RADIUS = 6371  # Radius of Earth in kilometers

def haversine(coordinates: List[float]) -> float:
  """Returns the great-circle or spherical distance (in km) between two 
  points on a sphere given their longitudes and latitudes using the 
  Haversine Formula.
  See https://en.wikipedia.org/wiki/Haversine_formula for more details.
  
  @params List[float] coordinates: the list of the coordinates of
  the two points for which we want to calculate the distance. 
  @return float: the spherical distance in km between the given two 
  points.
  """
  origin_lon, origin_lat, dest_lon, dest_lat = map(math.radians, coordinates)

  # Apply Haversine formula
  dist_lon = dest_lon - origin_lon
  dist_lat = dest_lat - origin_lat
  distance = math.sin(dist_lat/2)**2 + math.cos(origin_lat) * math.cos(dest_lat) * math.sin(dist_lon/2)**2
  distance = 2 * math.asin(math.sqrt(distance))
  
  distance *= EARTH_RADIUS  # Convert the distance in kilometers
  
  return distance