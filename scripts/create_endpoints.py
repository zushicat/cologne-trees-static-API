import json
from typing import Any, Dict, List

from _agegroup import create_agegroup_endpoints
from _districts import create_districts_endpoints
from _genus import create_genus_endpoints
from _meta import create_meta_endpoints
from _suburbs import create_suburbs_endpoints
from _object_type import create_object_type_endpoints
from _location_type import create_location_type_endpoints

from _utils import filter_cut_trees


def _load_data() -> List[Dict[str, Any]]:
    with open("../data/trees_cologne_merged.jsonln") as f:
        tree_data_str = f.read().split("\n")
    
    tree_data: List[Dict[str, Any]] = []
    for line in tree_data_str:
        try:
            current_tree = json.loads(line)
        except:
            pass
        tree_data.append(current_tree)
    
    return tree_data


if __name__ == "__main__":
    tree_data = _load_data()
    tree_data_2017, tree_data_2020 = filter_cut_trees(tree_data)  # tree_data_2017 == 2017 only
    
    create_agegroup_endpoints(tree_data_2017, tree_data_2020)
    create_districts_endpoints(tree_data_2017, tree_data_2020)
    create_genus_endpoints(tree_data_2017, tree_data_2020)
    create_suburbs_endpoints(tree_data_2017, tree_data_2020)
    create_meta_endpoints(tree_data_2017, tree_data_2020)
    create_object_type_endpoints(tree_data_2017, tree_data_2020)
    create_location_type_endpoints(tree_data_2017, tree_data_2020)
