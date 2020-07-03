import json
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data
from _utils import clean_key


ENDPOINT_GROUP = "agegroups"


def _count_trees(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        age_group = tree["tree_age"]["age_group_2020"]
        if age_group is None:
            if use_prediction is True:
                try:
                    age_group = tree["predictions"]["age_prediction"]["age_group_2020"]
                except:
                    try:
                        age_group = tree["predictions"]["by_radius_prediction"]["age_group_2020"]
                    except:
                        pass
        
        age_group = clean_key(age_group)

        if counted_trees.get(age_group) is None:
            counted_trees[age_group]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[age_group]["absolute"] += 1
    
    for age_group, vals in counted_trees.items():
        counted_trees[age_group]["percentage"] = round(vals["absolute"]/len(tree_data), 2)
    
    return counted_trees


def _count_age_group_by_district(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        age_group = tree["tree_age"]["age_group_2020"]
        if age_group is None:
            if use_prediction is True:
                try:
                    age_group = tree["predictions"]["age_prediction"]["age_group_2020"]
                except:
                    try:
                        age_group = tree["predictions"]["by_radius_prediction"]["age_group_2020"]
                    except:
                        pass
        
        age_group = clean_key(age_group)

        if counted_trees.get(age_group) is None:
            counted_trees[age_group]: Dict[str, Any] = {}

        district_name = clean_key(tree["geo_info"]["city_district"])

        if counted_trees[age_group].get(district_name) is None:
            counted_trees[age_group][district_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[age_group][district_name]["absolute"] += 1

    for agegroup, agegroup_vals in counted_trees.items():
        all_agegroup_trees = sum([x["absolute"] for x in agegroup_vals.values()])
        for district, vals in agegroup_vals.items():
            counted_trees[agegroup][district]["percentage"] = round(vals["absolute"]/all_agegroup_trees, 2)
    
    return counted_trees


def _count_age_group_by_genus(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        age_group = tree["tree_age"]["age_group_2020"]
        if age_group is None:
            if use_prediction is True:
                try:
                    age_group = tree["predictions"]["age_prediction"]["age_group_2020"]
                except:
                    try:
                        age_group = tree["predictions"]["by_radius_prediction"]["age_group_2020"]
                    except:
                        pass
        
        age_group = clean_key(age_group)
        
        if counted_trees.get(age_group) is None:
            counted_trees[age_group]: Dict[str, Any] = {}

        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            if use_prediction is True:
                try:
                    genus_name = tree["predictions"]["by_radius_prediction"]["genus"]
                except:
                    pass
        genus_name = clean_key(genus_name)
        
        if counted_trees[age_group].get(genus_name) is None:
            counted_trees[age_group][genus_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[age_group][genus_name]["absolute"] += 1

    for agegroup, agegroup_vals in counted_trees.items():
        all_agegroup_trees = sum([x["absolute"] for x in agegroup_vals.values()])
        for genus, vals in agegroup_vals.items():
            counted_trees[agegroup][genus]["percentage"] = round(vals["absolute"]/all_agegroup_trees, 2)
    
    return counted_trees


def create_agegroup_endpoints(tree_data_2017: List[Dict[str, Any]], tree_data_2020: List[Dict[str, Any]]) -> None:
    # ***
    #
    dat = _count_trees(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count")
    
    dat = _count_trees(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "tree_count_with_predictions")

    # ***
    #
    dat = _count_trees(tree_data_2017, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count")
    
    dat = _count_trees(tree_data_2017, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_count_with_predictions")


    # ***
    #
    dat = _count_age_group_by_district(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "districts")

    dat = _count_age_group_by_district(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "districts_with_predictions")


    # ***
    #
    dat = _count_age_group_by_genus(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "genus")

    dat = _count_age_group_by_genus(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "genus_with_predictions")
