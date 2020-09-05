'''

'''

import json
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data
from _utils import clean_key


ENDPOINT_GROUP = "location_type"


def _location_type(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    location_types_count: Dict[str, int] = {}
    for tree in tree_data:
        location_types = tree["tree_location_type"]
        
        if location_types is None:
            location_type = clean_key(location_types)
            if location_types_count.get(location_type) is None:
                location_types_count[location_type] = 0
            location_types_count[location_type] += 1
            continue

        is_highway = False
        if len(location_types) == 1 and "highway" in location_types:
            is_highway = True

        for location_type in location_types:
            if location_type == "highway" and is_highway is False:
                continue
            if location_types_count.get(location_type) is None:
                location_types_count[location_type] = 0
            location_types_count[location_type] += 1

    return location_types_count


def _osm_keys(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    osm_keys_count: Dict[str, int] = {}
    for tree in tree_data:
        location_types = tree["tree_location_type"]
        
        if location_types is None:
            location_type = clean_key(location_types)
            if osm_keys_count.get(location_type) is None:
                osm_keys_count[location_type] = 0
            osm_keys_count[location_type] += 1
            continue

        is_highway = False
        if len(location_types) == 1 and "highway" in location_types:
            is_highway = True

        for location_type, osm_node in location_types.items():
            if location_type == "highway" and is_highway is False:
                continue
            
            if is_highway is True:
                if osm_keys_count.get(location_type) is None:
                    osm_keys_count[location_type] = 0
                osm_keys_count[location_type] += 1
            else:
                osm_key = osm_node["type"]
                if osm_keys_count.get(osm_key) is None:
                    osm_keys_count[osm_key] = 0
                osm_keys_count[osm_key] += 1

    return osm_keys_count


def create_location_type_endpoints(tree_data_2017: List[Dict[str, Any]], tree_data_2020: List[Dict[str, Any]]) -> None:
    # ***
    #
    dat = _location_type(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count_location_type")

    dat = _location_type(tree_data_2017)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count_location_type")

    # ***
    #
    dat = _osm_keys(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count_osm_keys")

    dat = _osm_keys(tree_data_2017)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count_osm_keys")

