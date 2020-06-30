import json
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data


SUBSTITUTE_NONE_VALUE = "unknown"
ENDPOINT_GROUP = "agegroups"


def _clean_key(attr_key: Any) -> str:
    if attr_key is None:
        attr_key = SUBSTITUTE_NONE_VALUE
    else:
        attr_key = str(attr_key)
    return attr_key


def _filter_cut_trees(tree_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    '''
    Get 2 sets of tree data: still existing and not existing in 2020 (presumed cut down)
    '''
    trees_2017_only: List[Dict[str, Any]] = []
    trees_2020: List[Dict[str, Any]] = []

    for tree in tree_data:
        if tree["found_in_dataset"]["2017"] is True and tree["found_in_dataset"]["2020"] is False:
            trees_2017_only.append(tree)
        else:
            if tree["found_in_dataset"]["2020"] is True:
                trees_2020.append(tree)
    
    return trees_2017_only, trees_2020


def _count_age_groups(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_age_groups: Dict[str, int] = {}
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
        
        age_group = _clean_key(age_group)

        if counted_age_groups.get(age_group) is None:
            counted_age_groups[age_group] = 0
        counted_age_groups[age_group] += 1
    
    return counted_age_groups


def _count_age_group_by_district(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_age_group_by_districts: Dict[str, int] = {}
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
        
        age_group = _clean_key(age_group)

        if counted_age_group_by_districts.get(age_group) is None:
            counted_age_group_by_districts[age_group]: Dict[str, Any] = {}

        district_name = _clean_key(tree["geo_info"]["city_district"])

        if counted_age_group_by_districts[age_group].get(district_name) is None:
            counted_age_group_by_districts[age_group][district_name] = 0
        counted_age_group_by_districts[age_group][district_name] += 1
    
    return counted_age_group_by_districts


def _count_age_group_by_genus(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_age_group_by_genus: Dict[str, int] = {}
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
        
        age_group = _clean_key(age_group)
        
        if counted_age_group_by_genus.get(age_group) is None:
            counted_age_group_by_genus[age_group]: Dict[str, Any] = {}

        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            if use_prediction is True:
                try:
                    genus_name = tree["predictions"]["by_radius_prediction"]["genus"]
                except:
                    pass
        genus_name = _clean_key(genus_name)
        
        if counted_age_group_by_genus[age_group].get(genus_name) is None:
            counted_age_group_by_genus[age_group][genus_name] = 0
        counted_age_group_by_genus[age_group][genus_name] += 1
    
    return counted_age_group_by_genus



def create_agegroup_endpoints(tree_data: List[Dict[str, Any]]) -> None:
    tree_data_2017, tree_data_2020 = _filter_cut_trees(tree_data)
    
    # ***
    #
    dat = _count_age_groups(tree_data_2020, False)
    write_endpoint_data(dat, ENDPOINT_GROUP, "counted")
    
    dat = _count_age_groups(tree_data_2020, True)
    write_endpoint_data(dat, ENDPOINT_GROUP, "counted_with_predictions")


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
