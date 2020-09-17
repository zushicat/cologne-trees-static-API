'''

'''

import json
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data
from _utils import clean_key


ENDPOINT_GROUP = "object_type"
MIN_PROBABILITY = 0.5


def _count_object_type_by_age_group(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        object_type = tree["base_info"]["object_type"]
        object_type = clean_key(object_type)
        
        if counted_trees.get(object_type) is None:
            counted_trees[object_type]: Dict[str, Any] = {}
        
        age_group = tree["tree_age"]["age_group_2020"]
        if age_group is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["age_group"]["probability"] >= MIN_PROBABILITY:
                        age_group = tree["predictions"]["by_radius_prediction"]["age_group"]["prediction"]
                except:
                    pass
        
        age_group = clean_key(age_group)
        if counted_trees[object_type].get(age_group) is None:
            counted_trees[object_type][age_group]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[object_type][age_group]["absolute"] += 1

    for object_type, object_type_vals in counted_trees.items():
        all_object_type_trees = sum([x["absolute"] for x in object_type_vals.values()])
        for agegroup, vals in object_type_vals.items():
            counted_trees[object_type][agegroup]["percentage"] = round(vals["absolute"]/all_object_type_trees, 2)
    
    return counted_trees


def _count_object_type_by_district(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        object_type = tree["base_info"]["object_type"]
        object_type = clean_key(object_type)

        if counted_trees.get(object_type) is None:
            counted_trees[object_type]: Dict[str, Any] = {}

        district_name = clean_key(tree["geo_info"]["district"])
        
        if counted_trees[object_type].get(district_name) is None:
            counted_trees[object_type][district_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[object_type][district_name]["absolute"] += 1

    for object_type, object_type_vals in counted_trees.items():
        all_object_type_trees = sum([x["absolute"] for x in object_type_vals.values()])
        for district, vals in object_type_vals.items():
            counted_trees[object_type][district]["percentage"] = round(vals["absolute"]/all_object_type_trees, 2)
    
    return counted_trees


def _count_object_type_by_suburb(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        object_type = tree["base_info"]["object_type"]
        object_type = clean_key(object_type)

        if counted_trees.get(object_type) is None:
            counted_trees[object_type]: Dict[str, Any] = {}

        suburb_name = clean_key(tree["geo_info"]["suburb"])
        
        if counted_trees[object_type].get(suburb_name) is None:
            counted_trees[object_type][suburb_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[object_type][suburb_name]["absolute"] += 1

    for object_type, object_type_vals in counted_trees.items():
        all_object_type_trees = sum([x["absolute"] for x in object_type_vals.values()])
        for suburb, vals in object_type_vals.items():
            counted_trees[object_type][suburb]["percentage"] = round(vals["absolute"]/all_object_type_trees, 2)
    
    return counted_trees


def _count_trees(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        object_type = tree["base_info"]["object_type"]
        object_type = clean_key(object_type)

        if counted_trees.get(object_type) is None:
            counted_trees[object_type]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[object_type]["absolute"] += 1
    
    for object_type, vals in counted_trees.items():
        counted_trees[object_type]["percentage"] = round(vals["absolute"]/len(tree_data), 2)
    
    return counted_trees


def _object_type_count_year_planting(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    tree_list: Dict[str, Dict[str, Dict[str, int]]] = {}
    
    for tree in tree_data:
        object_type = tree["base_info"]["object_type"]
        if object_type is None:
            continue

        bole_radius = tree["tree_measures"]["bole_radius"]
        if bole_radius is None:
            continue

        if use_prediction is False:
            year_planting = tree["base_info"]["year_planting"]
        else:
            try:
                year_planting = tree["tree_age"]["year_sprout"]
            except:
                pass
        if year_planting is None:
            continue

        if tree_list.get(object_type) is None:
            tree_list[object_type]: Dict[str, Dict[str, int]] = {}
        
        if tree_list[object_type].get(bole_radius) is None:
            tree_list[object_type][bole_radius]: Dict[str, int] = {}

        if tree_list[object_type][bole_radius].get(year_planting) is None:
            tree_list[object_type][bole_radius][year_planting]: int = 0
        
        tree_list[object_type][bole_radius][year_planting] += 1

    return tree_list


def create_object_type_endpoints_inventory(tree_data_2017: List[Dict[str, Any]], tree_data_2020: List[Dict[str, Any]]) -> None:
    # ***
    #
    dat = _count_trees(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count")

    # ***
    #
    dat = _count_trees(tree_data_2017)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count")

    # ***
    #
    dat = _count_object_type_by_district(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "district")

    # ***
    #
    dat = _count_object_type_by_suburb(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "suburb")

    # ***
    #
    dat = _count_object_type_by_age_group(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "age_groups")

    dat = _count_object_type_by_age_group(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "age_groups_with_prediction")
    
    # ***
    #
    dat = _object_type_count_year_planting(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "ground_truth_bole_radius_year_planting")

    dat = _object_type_count_year_planting(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "regression_bole_radius_year_sprout")
    