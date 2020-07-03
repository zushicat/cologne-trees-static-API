from typing import Any, Dict, List, Tuple


SUBSTITUTE_NONE_VALUE = "unknown"


def clean_key(attr_key: Any) -> str:
    if attr_key is None:
        attr_key = SUBSTITUTE_NONE_VALUE
    else:
        attr_key = str(attr_key)
    return attr_key


def filter_cut_trees(tree_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
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