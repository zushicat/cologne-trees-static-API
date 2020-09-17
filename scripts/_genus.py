'''

'''

import json
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data
from _utils import clean_key


ENDPOINT_GROUP = "genus"
MIN_PROBABILITY = 0.5


def _count_genus_by_age_group(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["genus"]["probability"] >= MIN_PROBABILITY:
                        genus_name = tree["predictions"]["by_radius_prediction"]["genus"]["prediction"]
                except:
                    pass
        genus_name = clean_key(genus_name)
        
        if counted_trees.get(genus_name) is None:
            counted_trees[genus_name]: Dict[str, Any] = {}
        
        age_group = tree["tree_age"]["age_group_2020"]
        if age_group is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["age_group"]["probability"] >= MIN_PROBABILITY:
                        age_group = tree["predictions"]["by_radius_prediction"]["age_group"]["prediction"]
                except:
                    pass
        
        age_group = clean_key(age_group)
        if counted_trees[genus_name].get(age_group) is None:
            counted_trees[genus_name][age_group]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[genus_name][age_group]["absolute"] += 1

    for genus, genus_vals in counted_trees.items():
        all_genus_trees = sum([x["absolute"] for x in genus_vals.values()])
        for agegroup, vals in genus_vals.items():
            counted_trees[genus][agegroup]["percentage"] = round(vals["absolute"]/all_genus_trees, 2)
    
    return counted_trees


def _count_genus_by_district(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["genus"]["probability"] >= MIN_PROBABILITY:
                        genus_name = tree["predictions"]["by_radius_prediction"]["genus"]["prediction"]
                except:
                    pass
        genus_name = clean_key(genus_name)

        if counted_trees.get(genus_name) is None:
            counted_trees[genus_name]: Dict[str, Any] = {}

        district_name = clean_key(tree["geo_info"]["district"])
        
        if counted_trees[genus_name].get(district_name) is None:
            counted_trees[genus_name][district_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[genus_name][district_name]["absolute"] += 1

    for genus, genus_vals in counted_trees.items():
        all_genus_trees = sum([x["absolute"] for x in genus_vals.values()])
        for district, vals in genus_vals.items():
            counted_trees[genus][district]["percentage"] = round(vals["absolute"]/all_genus_trees, 2)
    
    return counted_trees


def _count_trees(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["genus"]["probability"] >= MIN_PROBABILITY:
                        genus_name = tree["predictions"]["by_radius_prediction"]["genus"]["prediction"]
                except:
                    pass
        genus_name = clean_key(genus_name)

        if counted_trees.get(genus_name) is None:
            counted_trees[genus_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[genus_name]["absolute"] += 1
    
    for genus, vals in counted_trees.items():
        counted_trees[genus]["percentage"] = round(vals["absolute"]/len(tree_data), 2)
    
    return counted_trees


def _bole_radius_count_year_planting(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    tree_list: Dict[str, Dict[str, Dict[str, int]]] = {}
    
    for tree in tree_data:
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
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

        if tree_list.get(genus_name) is None:
            tree_list[genus_name]: Dict[str, Dict[str, int]] = {}
        
        if tree_list[genus_name].get(bole_radius) is None:
            tree_list[genus_name][bole_radius]: Dict[str, int] = {}

        if tree_list[genus_name][bole_radius].get(year_planting) is None:
            tree_list[genus_name][bole_radius][year_planting]: int = 0
        
        tree_list[genus_name][bole_radius][year_planting] += 1

    return tree_list


def create_genus_endpoints_inventory(tree_data_2017: List[Dict[str, Any]], tree_data_2020: List[Dict[str, Any]]) -> None:
    # ***
    #
    dat = _count_trees(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count")

    dat = _count_trees(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count_with_prediction")

    # ***
    #
    dat = _count_trees(tree_data_2017, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count")

    dat = _count_trees(tree_data_2017, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count_with_prediction")

    # ***
    #
    dat = _count_genus_by_district(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "district")

    dat = _count_genus_by_district(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "district_with_prediction")

    # ***
    #
    dat = _count_genus_by_age_group(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "age_groups")

    dat = _count_genus_by_age_group(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "age_groups_with_prediction")
    
    # ***
    #
    dat = _bole_radius_count_year_planting(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "ground_truth_bole_radius_year_planting")

    dat = _bole_radius_count_year_planting(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "regression_bole_radius_year_sprout")
    