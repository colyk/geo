#!/usr/bin/env python3

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.api import Api
import json

from collections import OrderedDict

nominatim = Nominatim()
overpass = Overpass()
api = Api()


def choose_relation(area, type):
    area_json = nominatim.query(area).toJSON()
    answer = None
    #print(json.dumps(area_json, indent=4, sort_keys=True))
    for obj in area_json:
        if(obj['osm_type'] == 'relation'):
            print('Are you looking for', obj['display_name'] + ',', obj['type'] + ',', obj['osm_id'], '? - :')
            answer = input()
            if(answer is 'y'):
                break
        else:
            break
    if(answer is None):
        print("Nothing found")
        return None;
    if(answer is not 'y'):
        print("There is no other areas")
        return None;
    relation = api.query("relation/" + str(obj['osm_id'])).tags()
    selector = type_to_selector(type)
    if selector is None:
        print("Wrong place type")
        return None
    return {'rel': relation, 'sel': selector}


def fetch_data_by_relation(relation, selector, element_type):
    query = overpassQueryBuilder(area='REPLACE_TEXT', elementType=element_type, selector=selector, out='')
    query = query.replace('(REPLACE_TEXT)', build_area_selector(relation))
    return overpass.query(query, timeout=60).toJSON()


def build_area_selector(relation):
    area_selector = ''
    for obj in relation:
        area_selector += '["' + obj + '"="' + relation[obj] + '"]'
    return area_selector


def type_to_selector(type):
    #if(type==""):
    #    return '""=""';
    if(type=="attraction"):
        return '"tourism"="attraction"';
    if(type=="museum"):
        return '"tourism"="museum"';
    if(type=="theatre"):
        return '"amenity"="theatre"';
    if(type=="restaurant"):
        return '"amenity"="restaurant"';
    if(type=="mall"):
        return '"shop"="mall"';
    if(type=="supermarket"):
        return '"shop"="supermarket"';
    if(type=="university"):
        return '"amenity"="university"';
    if(type=="school"):
        return '"amenity"="school"';
    if(type=="kindergarten"):
        return '"amenity"="kindergarten"';
    if(type=="castle"):
        return '"historic"="castle"';
    if(type=="catholic_place"):
        return '"denomination"="roman_catholic"';
    if(type=="parking"):
        return '"amenity"="parking"';
    if(type=="bank"):
        return '"amenity"="bank"';
    if(type=="bus"):
        return '"route"="bus"';
    if(type=="trolleybus"):
        return '"route"="trolleybus"';
    if(type=="polish_city"):
        return '"name:prefix"="miasto"';
    return None

if __name__ == '__main__':
    fetch_pack = choose_relation("Polska", "polish_city")
    data = fetch_data_by_relation(fetch_pack['rel'], fetch_pack['sel'], 'relation')
    print(json.dumps(data, indent=4, sort_keys=True))
