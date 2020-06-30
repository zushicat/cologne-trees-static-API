'''
def _count_age_group_by_district(tree_data: List[Dict[str, Any]], use_prediction: bool) -> Dict[str, Any]:
    counted_age_group_by_districts: Dict[str, int] = {}
    for tree in tree_data:
        district_name = _clean_key(tree["geo_info"]["city_district"])
        if counted_age_group_by_districts.get(district_name) is None:
            counted_age_group_by_districts[district_name]: Dict[str, Any] = {}
        
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
        if counted_age_group_by_districts[district_name].get(age_group) is None:
            counted_age_group_by_districts[district_name][age_group] = 0
        counted_age_group_by_districts[district_name][age_group] += 1
    
    return counted_age_group_by_districts
'''