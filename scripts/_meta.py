import json
from statistics import mean, median
from typing import Any, Dict, List, Tuple

from _save_endpoint_data import write_endpoint_data
from _utils import clean_key


ENDPOINT_GROUP = "meta"


def _completeness(tree_data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    completeness_list: Dict[str, Any] = {
        "dataset_completeness": {"tmp_list": []},
        "base_info_completeness": {"tmp_list": []},
        "tree_taxonomy_completeness": {"tmp_list": []},
        "tree_measures_completeness": {"tmp_list": []},
        "tree_age_completeness": {"tmp_list": []}
    }
    for tree in tree_data:
        for completeness in ["dataset_completeness", "base_info_completeness", "tree_taxonomy_completeness", "tree_measures_completeness", "tree_age_completeness"]:
            completeness_list[completeness]["tmp_list"].append(tree[completeness])
    
    for completeness in ["dataset_completeness", "base_info_completeness", "tree_taxonomy_completeness", "tree_measures_completeness", "tree_age_completeness"]:
        completeness_list[completeness]["mean"] = round(mean(completeness_list[completeness]["tmp_list"]), 2)
        completeness_list[completeness]["median"] = median(completeness_list[completeness]["tmp_list"])

        del completeness_list[completeness]["tmp_list"]
    
    return completeness_list


# ************
# geo
# ************
def _districts_suburbs(tree_data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    suburbs_in_district: Dict[str, List[str]] = {}
    for tree in tree_data:
        district_name = tree["geo_info"]["city_district"]

        if district_name is None:
            continue

        if suburbs_in_district.get(district_name) is None:
            suburbs_in_district[district_name]: List[str] = []
        
        suburb_name = tree["geo_info"]["suburb"]
        if suburb_name not in suburbs_in_district[district_name] and suburb_name is not None:
            suburbs_in_district[district_name].append(suburb_name)
    return suburbs_in_district


def _suburb_district(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    suburb_list: Dict[str, str] = {}
    for tree in tree_data:
        suburb_name = tree["geo_info"]["suburb"]
        if suburb_name is None:
            continue

        if suburb_list.get(suburb_name) is None:
            suburb_list[suburb_name]: str = tree["geo_info"]["city_district"]
        else:
            continue
        
    return suburb_list


def _district_data_completeness(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    completeness_in_district: Dict[str, List[str]] = {}
    for tree in tree_data:
        district_name = clean_key(tree["geo_info"]["city_district"])

        # if district_name is None:
        #     continue

        if completeness_in_district.get(district_name) is None:
            completeness_in_district[district_name]: Dict[str, Any] = {
                "mean": None,
                "median": None,
                "min": None,
                "max": None,
                "tmp_list": []
            }
        
        dataset_completeness = tree["dataset_completeness"]
        completeness_in_district[district_name]["tmp_list"].append(dataset_completeness)

    for district, vals in completeness_in_district.items():
        completeness_in_district[district]["min"] = min(vals["tmp_list"])
        completeness_in_district[district]["max"] = max(vals["tmp_list"])
        completeness_in_district[district]["mean"] = round(mean(vals["tmp_list"]), 2)
        completeness_in_district[district]["median"] = median(vals["tmp_list"])

        del completeness_in_district[district]["tmp_list"]
    
    return completeness_in_district


def _suburb_data_completeness(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    completeness_in_suburb: Dict[str, List[str]] = {}
    for tree in tree_data:
        suburb_name = clean_key(tree["geo_info"]["suburb"])

        # if suburb_name is None:
        #     continue

        if completeness_in_suburb.get(suburb_name) is None:
            completeness_in_suburb[suburb_name]: Dict[str, Any] = {
                "mean": None,
                "median": None,
                "min": None,
                "max": None,
                "tmp_list": []
            }
        
        dataset_completeness = tree["dataset_completeness"]
        completeness_in_suburb[suburb_name]["tmp_list"].append(dataset_completeness)

    for suburb, vals in completeness_in_suburb.items():
        completeness_in_suburb[suburb]["min"] = min(vals["tmp_list"])
        completeness_in_suburb[suburb]["max"] = max(vals["tmp_list"])
        completeness_in_suburb[suburb]["mean"] = round(mean(vals["tmp_list"]), 2)
        completeness_in_suburb[suburb]["median"] = median(vals["tmp_list"])

        del completeness_in_suburb[suburb]["tmp_list"]
    
    return completeness_in_suburb


# ************
# taxonomy
# ************
def _genus_name_german(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    names_list: Dict[str, int] = {}
    for tree in tree_data:
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            continue

        if names_list.get(genus_name) is None:
            names_list[genus_name]: List[str] = []
        
        name_german_list = tree["tree_taxonomy"]["name_german"]
        
        if name_german_list is None:
            continue

        for name_german in name_german_list:
            if name_german not in names_list[genus_name]:
                names_list[genus_name].append(name_german)

    # ***
    # default for empty values: null
    for key, vals in names_list.items():
        if len(vals) == 0:
            names_list[key] = None

    return names_list


def _species_name_german(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    names_list: Dict[str, int] = {}
    for tree in tree_data:
        species_name = tree["tree_taxonomy"]["species"]
        if species_name is None:
            continue

        
        if names_list.get(species_name) is None:
            names_list[species_name]: List[str] = []
        
        name_german_list = tree["tree_taxonomy"]["name_german"]
        if name_german_list is None:
            continue
        
        for name_german in name_german_list:
            if name_german not in names_list[species_name]:
                names_list[species_name].append(name_german)
    
    # ***
    # default for empty values: null
    for key, vals in names_list.items():
        if len(vals) == 0:
            names_list[key] = None

    return names_list


def _name_german_genus(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    names_list: Dict[str, int] = {}
    for tree in tree_data:
        name_german_list = tree["tree_taxonomy"]["name_german"]
        if name_german_list is None:
            continue

        for name_german in name_german_list:
            if names_list.get(name_german) is None:
                names_list[name_german]: str = tree["tree_taxonomy"]["genus"]
            else:
                continue
        
    return names_list


def _name_german_species(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    names_list: Dict[str, int] = {}
    for tree in tree_data:
        name_german_list = tree["tree_taxonomy"]["name_german"]
        if name_german_list is None:
            continue

        for name_german in name_german_list:
            if names_list.get(name_german) is None:
                names_list[name_german]: str = tree["tree_taxonomy"]["species"]
            else:
                continue
        
    return names_list


def _genus_species_name_german_tree(tree_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    names_tree: Dict[str, int] = {}
    for tree in tree_data:
        genus_name = tree["tree_taxonomy"]["genus"]
        if genus_name is None:
            continue
        
        if names_tree.get(genus_name) is None:
            names_tree[genus_name]: Dict[str, List[str]] = {}
        
        species_name = clean_key(tree["tree_taxonomy"]["species"])
        if names_tree[genus_name].get(species_name) is None:
            names_tree[genus_name][species_name] = []

        name_german_list = tree["tree_taxonomy"]["name_german"]
        if name_german_list is None:
            continue
        
        for name_german in name_german_list:
            if name_german not in names_tree[genus_name][species_name]:
                names_tree[genus_name][species_name].append(name_german)
    
    # ***
    # default for empty values: null
    for genus_key, genus_vals in names_tree.items():
        for species_key, species_vals in genus_vals.items():
            if len(species_vals) == 0:
                names_tree[genus_key][species_key] = None

    return names_tree



def create_meta_endpoints(tree_data_2017: List[Dict[str, Any]], tree_data_2020: List[Dict[str, Any]]) -> None:
    # ***
    #
    dat = _districts_suburbs(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "districts_suburbs")

    # ***
    #
    dat = _suburb_district(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "suburbs_districts")

    # ***
    #
    dat = _genus_name_german(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "genus_name_german")

    # ***
    #
    dat = _species_name_german(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "species_name_german")

    # ***
    #
    dat = _name_german_genus(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "name_german_genus")

    dat = _name_german_species(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "name_german_species")

    # ***
    #
    dat = _genus_species_name_german_tree(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "taxonomy")
    
    # ***
    #
    dat = _district_data_completeness(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "district_data_completeness")

    dat = _suburb_data_completeness(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "suburb_data_completeness")
    
    # ***
    #
    dat = _completeness(tree_data_2020)
    write_endpoint_data(dat, ENDPOINT_GROUP, "data_completeness")

