import json
from typing import Any, Dict, List

from _agegroup import create_agegroup_endpoints


def _load_data() -> List[Dict[str, Any]]:
    with open("../data/trees_cologne_merged.jsonl") as f:
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
    
    create_agegroup_endpoints(tree_data)