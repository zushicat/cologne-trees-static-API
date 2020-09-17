'''
Naming convention:
- tree inventory data: trees_cologne_inventory.jsonln
- tree detection data: trees_cologne_detection_{year}.jsonln (i.e. trees_cologne_detection_2019.jsonln)
'''

import json
from typing import Any, Dict, List

from _agegroup import create_agegroup_endpoints_inventory
from _districts import create_districts_endpoints_inventory
from _genus import create_genus_endpoints_inventory
from _meta import create_meta_endpoints_inventory
from _suburbs import create_suburbs_endpoints_inventory
from _object_type import create_object_type_endpoints_inventory
from _location_type import create_location_type_endpoints_inventory, create_location_type_endpoints_detection

from _utils import filter_cut_trees


def _load_data(file_name: str) -> List[Dict[str, Any]]:
    with open(f"../data/{file_name}") as f:
        tree_data_str = f.read().split("\n")
    
    tree_data: List[Dict[str, Any]] = []
    for line in tree_data_str:
        try:
            current_tree = json.loads(line)
        except:
            pass
        tree_data.append(current_tree)
    
    return tree_data


def create_inventory_data(file_name: str) -> None:
    '''
    Data from tree inventories is processed different than detection data
    '''
    tree_data = _load_data(file_name)
    tree_data_2017, tree_data_2020 = filter_cut_trees(tree_data)  # tree_data_2017 == 2017 only
    
    create_agegroup_endpoints(tree_data_2017, tree_data_2020)
    create_districts_endpoints(tree_data_2017, tree_data_2020)
    create_genus_endpoints(tree_data_2017, tree_data_2020)
    create_suburbs_endpoints(tree_data_2017, tree_data_2020)
    create_meta_endpoints(tree_data_2017, tree_data_2020)
    create_object_type_endpoints(tree_data_2017, tree_data_2020)
    create_location_type_endpoints(tree_data_2017, tree_data_2020)


def create_detection_data(file_name: str, year: str) -> None:
    print(file_name)
    tree_data = _load_data(file_name)
    create_location_type_endpoints_detection(tree_data, year)


if __name__ == "__main__":
    # create_inventory_data("trees_cologne_inventory.jsonln")
    create_detection_data("trees_cologne_detection_2019.jsonln", "2019")
