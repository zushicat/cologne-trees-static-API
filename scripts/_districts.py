import json
from statistics import mean, median
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data
from _utils import clean_key


ENDPOINT_GROUP = "districts"
MIN_PROBABILITY = 0.5


def _count_district_by_age_group(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        district_name = clean_key(tree["geo_info"]["district"])
        if counted_trees.get(district_name) is None:
            counted_trees[district_name]: Dict[str, Any] = {}
        
        age_group = tree["tree_age"]["age_group_2020"]
        if age_group is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["age_group"]["probability"] >= MIN_PROBABILITY:
                        age_group = tree["predictions"]["by_radius_prediction"]["age_group"]["prediction"]
                except:
                    pass
        
        age_group = clean_key(age_group)
        if counted_trees[district_name].get(age_group) is None:
            counted_trees[district_name][age_group]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[district_name][age_group]["absolute"] += 1

    for district, district_vals in counted_trees.items():
        all_district_trees = sum([x["absolute"] for x in district_vals.values()])
        for agegroup, vals in district_vals.items():
            counted_trees[district][agegroup]["percentage"] = round(vals["absolute"]/all_district_trees, 2)
    
    return counted_trees


def _count_district_by_genus(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        district_name = clean_key(tree["geo_info"]["district"])
        if counted_trees.get(district_name) is None:
            counted_trees[district_name]: Dict[str, Any] = {}
        
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            if use_prediction is True:
                try:
                    if tree["predictions"]["by_radius_prediction"]["genus"]["probability"] >= MIN_PROBABILITY:
                        genus_name = tree["predictions"]["by_radius_prediction"]["genus"]["prediction"]
                except:
                    pass
        genus_name = clean_key(genus_name)
        
        if counted_trees[district_name].get(genus_name) is None:
            counted_trees[district_name][genus_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[district_name][genus_name]["absolute"] += 1

    for district, district_vals in counted_trees.items():
        all_district_trees = sum([x["absolute"] for x in district_vals.values()])
        for genus, vals in district_vals.items():
            counted_trees[district][genus]["percentage"] = round(vals["absolute"]/all_district_trees, 2)
    
    return counted_trees


def _count_district_by_object_type(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        district_name = clean_key(tree["geo_info"]["district"])
        if counted_trees.get(district_name) is None:
            counted_trees[district_name]: Dict[str, Any] = {}
        
        object_type = tree["base_info"]["object_type"]
        object_type = clean_key(object_type)
        
        if counted_trees[district_name].get(object_type) is None:
            counted_trees[district_name][object_type]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[district_name][object_type]["absolute"] += 1

    for district, district_vals in counted_trees.items():
        all_district_trees = sum([x["absolute"] for x in district_vals.values()])
        for object_type, vals in district_vals.items():
            counted_trees[district][object_type]["percentage"] = round(vals["absolute"]/all_district_trees, 2)
    
    return counted_trees


def _count_trees(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        district_name = clean_key(tree["geo_info"]["district"])
        if counted_trees.get(district_name) is None:
            counted_trees[district_name]: Dict[str, Any] = {
                "absolute": 0,
                "percentage": 0
            }
        counted_trees[district_name]["absolute"] += 1

    for district, vals in counted_trees.items():
        counted_trees[district]["percentage"] = round(vals["absolute"]/len(tree_data), 2)
    
    return counted_trees


def _count_neighbours_radius_50(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    '''
    TODO: include this attribute in base data again
    '''
    counted_trees: Dict[str, int] = {}
    for tree in tree_data:
        district_name = clean_key(tree["geo_info"]["district"])

        if counted_trees.get(district_name) is None:
            counted_trees[district_name]: Dict[str, Any] = {
                "min": None,
                "max": None,
                "mean": None,
                "median": None,
                "tmp_list": []
            }
        
        num_neighbours = tree["num_neighbours_radius_50"]  # not included in base data right now
        if num_neighbours is None:
            continue
        
        counted_trees[district_name]["tmp_list"].append(num_neighbours)
    
    for district, vals in counted_trees.items():
        counted_trees[district]["min"] = min(vals["tmp_list"])
        counted_trees[district]["max"] = max(vals["tmp_list"])
        counted_trees[district]["mean"] = round(mean(vals["tmp_list"]))
        counted_trees[district]["median"] = median(vals["tmp_list"])

        del counted_trees[district]["tmp_list"]
    
    return counted_trees


def create_districts_endpoints(tree_data_2017: List[Dict[str, Any]], tree_data_2020: List[Dict[str, Any]]) -> None:
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
    dat = _count_district_by_genus(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "genus")

    dat = _count_district_by_genus(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "genus_with_predictions")

    dat = _count_district_by_genus(tree_data_2017, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_genus")

    dat = _count_district_by_genus(tree_data_2017, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_genus_with_predictions")

    # ***
    #
    dat = _count_district_by_age_group(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "age_groups")

    dat = _count_district_by_age_group(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "age_groups_with_predictions")

    dat = _count_district_by_age_group(tree_data_2017, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_age_groups")

    dat = _count_district_by_age_group(tree_data_2017, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "cut_tree_age_groups_with_predictions")

    # ***
    #
    # dat = _count_neighbours_radius_50(tree_data_2020)
    # write_endpoint_data(dat, ENDPOINT_GROUP, "density_neighbours_radius_50")
    
    # ***
    #
    dat = _count_district_by_object_type(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "object_type")
