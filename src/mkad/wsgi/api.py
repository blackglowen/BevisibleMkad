#!/usr/bin/env python
#-*- coding: utf-8 -*-

from typing import Dict, List, Any, NoReturn, Text, Tuple, Union
from flask import (render_template, abort, Blueprint)
import requests
import json
import math

from . import helpers

API_KEY = 'a23d5c7b-a217-4165-bd4e-9a8196a69b57' 
FORMAT = 'json'
LANG = 'en-US'
HOST = 'https://geocode-maps.yandex.ru/1.x/'

LOG_FILE = '.log'

# This constant holds the circumference of Moscow Ring Road in km.
# It is needed for dertermining the radius of the MKAD according 
# to the following formula: c = 2*r*pi => r = c / (2*pi)
MKAD_CIRCUMFERENCE =  108.9  # (67.7 mi)

bp = Blueprint('api', __name__, url_prefix='/mkad/api')


def is_invalid_address(addr: str) -> bool:
    """Returns True when the given address is invalid, False otherwise.
    The given address is considered invalid if it contains any forbidden 
    specials characters.
    
    @param str addr: address to be parsed
    @return bool
    """
    forbidden = '!"#$%&()*+£;<=>?@[\\]^_{|}~'
    return any(c in forbidden for c in addr)


def spherical_distance(coordinates: List[float]) -> float:
    """Returns the great-circle distance, orthodromic distance, or 
    spherical distance, which is the shortest distance between two 
    points on the surface of a sphere, measured along the surface of
    the sphere.
    
    @param List[float] coordinates: the list of the coordinates of
    the two points for which we want to calculate the distance 
    @return float: the spherical distance in km between the two points
    """
    return helpers.haversine(coordinates)
 

def get_coordinates(addr: str) -> Union[List[Dict[str, Any]], NoReturn]:
    """Returns the list of addresses (and their geographical coordinates) 
    that match the given address as a parameter. The matches and all the
    geographical informations are fetched from Yandex via their Geocoder 
    HTTP API. If any error occurs during the API call, then the request
    is aborted and the function returns a NoRuturn object.
    
    @param str addr: address for which we want to find the distance from MKAD
    @return Union[List, NoReturn]: list of matched addresses or NoReturn object
    """
    found = []  # This is container for matches or matched addresses.
    
    # Set the request host and parameters, then make a GET HTTP call to HOST.
    # Here while setting the api key and other parameters, we make sure to set
    # the response format to json to facilitate its manipulation.
    response = requests.get(HOST, 
                            params={'apikey': API_KEY, 'format': FORMAT, 
                                    'geocode': addr, 'lang': LANG})
    if(response.status_code == 200):
        # If the request status is OK (meaning no error occured), then convert 
        # the response text in json format into the convenient Python object.
        # After that, according to the Geocoder HTTP API description, use the 
        # convenient keys to retrieve address informations such longitude, 
        # latitude, country code, etc.
        # Each retrieved matched address is added to the found list, which is
        # returned after all iterations. 
        json_result = json.loads(response.text)
        collection = json_result['response']['GeoObjectCollection']
        for geoObject in collection['featureMember']:
            geoObject = geoObject['GeoObject']
            address = {}
            address['name'] = geoObject['name']
            address['desc'] = geoObject['description']
            address['long'], address['lat'] = tuple(geoObject['Point']['pos'].split())
            address['long'] = float(address['long'])
            address['lat'] = float(address['lat'])
            found.append(address)
    else:
      # This portion of code is exceuted only in case of any HTTP Error during the API call.
      # In which case the function aborts the request with the response status code and returns
      # an instance of NoReturn type.
      return  abort(response.status_code)

    return found

def get_origin_coordinates()-> Dict[str, Any]:
    """Return the coordinates and other geographical information
    of the MKAD as dictionary. This is considered to be the origin 
    or the point from which the distance to other places is calculated.
    
    @return Dict[str, Any]: a dictionary representing the origin 
    """
    # Here Moscow is considered to be the center of the ring.
    # So basically, all the distances to other addresses is 
    # determined from this point.
    origin = get_coordinates('Moscow')
    return origin[0]
  
def calculate_mkad_distance(matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Caculates, then sets the spherical distance from MKAD as origin for all 
    matches or matched addresses.
    """
    origin = get_origin_coordinates()
    
    # Here knowing the circumference of the MKAD, we can easily determine its 
    # radius. And any distance, from origin to a given matched address, less or 
    # equal to the radius the MKAD is considered to be inside the MKAP perimeter.
    # If so we mark the distance for the matched address as inside MKAD by setting
    # its distance to 0 (zero).
    radius = MKAD_CIRCUMFERENCE/(2*math.pi)
    with open(LOG_FILE, 'a') as log:
        for m in matches:
            d = spherical_distance([origin['long'], origin['lat'], m['long'], m['lat']])
            if d <= radius:
                d = 0
            m['dist'] = d
            log.writelines(m['name'] + ', ' +  m['desc'] + ', ' + 'long=' +str(m['long']) +
                        ', ' + 'lat=' + str(m['lat']) + ', distance='+ str(m['dist']) + ' km' + '\n') 
        log.close()
    return matches

# Fisrt bind, with route decorator, the api blueprint to this function to find all 
# matches of the given address.
# Then the function checks whether the input address is valid or not. 
# If the address is proved invalid the function renders the error view or page with
# an error message, otherwise it continues by looking for matches and calculates 
# the distance that seperates each match from MKAD origin.
# Finally the matches are passed in to the results view for displaying them. 
@bp.route("/<addr>")
def find_matched_addresses(addr: str) -> Text:
    if(is_invalid_address(addr)):
        return render_template(
            'error.html',
            error = "The given address '" + addr + 
                     "' is invalid. Please provide one with no special characters.")
    
    matches = get_coordinates(addr)
    matches = calculate_mkad_distance(matches)
    return render_template('result.html', address=addr, found=matches)