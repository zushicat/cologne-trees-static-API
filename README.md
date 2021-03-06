# cologne-trees-static-API
A static API to request aggregated information about city trees in Cologne, Germany by endpoints.

For information about the creation of the underlaying data used for this aggregation, please refer to this repository:    
https://github.com/zushicat/cologne-trees-data    

If you like to see a visualization of this data, please refer following html version of this repository:    
https://zushicat.github.io/cologne-tree-map/    


You can access an enpoint by requesting:    
```
https://zushicat.github.io/cologne-trees-static-API/endpoints/{group name}/{endpoint name}.json
```

Example:
```
https://zushicat.github.io/cologne-trees-static-API/endpoints/genus/tree_count.json
```

The completeness of the underlaying datasets varies, hence blind spots are predicted by different methods, applied to:
- agegroup
- genus

To see the variance in the original data (per genus) within bole radius and (usually) estimated age (and counted occurances) ( transferred to year planted) please see:    
[genus / ground_truth_bole_radius_year_planting.json](https://zushicat.github.io/cologne-trees-static-API/endpoints/genus/ground_truth_bole_radius_year_planting.json)    

When genus and bole radius are available, age related values are derived from a regression model. Otherwise, the significantly less precise method of estimation by neighbouring tree clusters in a radius of 50 meter around the respective tree is applied.    
Only predictions with a probability >= 0.5 are taken into account.    

The latter predictions can get requested seperately (i.e. "tree_count" vs. "tree_count_with_predictions").    

Additionally, the assumption is made that if a tree is occuring in the dataset of 2017 but not in the dataset of 2020, then this tree most likely is cut down at some point within the 3 years timespan.   
(Still, this is just an assumption and should be treated as such.)    

These trees can be separately requested (i.e. "cut_tree_count" bs. "tree_count")    
Otherwise, only trees occuring in the newest 2020 dataset (resp. both datasets) are used in the response.


## Endpoints
The endpoints are bundled in 5 groups:
- agegroups
- districts
- suburbs
- genus
- meta


The endpoints often reflect a different perspective on the same data relationships, simply making usage for different scenarios more convenient (compare i.e. "agegroups / districts" vs. "districts / age_groups").    


### agegroups
The ages of trees (if known) are grouped as followed:
- 0: <= 25
- 1: 26 - 40
- 2: >= 40

or "unknown"    

These values are not derived from the (usually) estimated age values in the original datasets but predicted with a regression of genus and bole radius (X) and age of a tree (y).    
The endpoint genus_with_predictions uses predicted values both for agegroup and genus, otherwise _with_predictions indicates the usage of predicted agegroups.


```
agegroups / tree_count
agegroups / tree_count_with_predictions
agegroups / cut_tree_count
agegroups / cut_tree_count_with_predictions
agegroups / districts
agegroups / districts_with_predictions
agegroups / genus
agegroups / genus_with_predictions
agegroups / object_type
agegroups / object_type_with_predictions
```

### districts
Aggregations collected under city districts.    

```
districts / tree_count
districts / cut_tree_count
districts / genus
districts / genus_with_predictions
districts / cut_tree_genus
districts / cut_tree_genus_with_predictions
districts / age_groups
districts / age_groups_with_predictions
districts / cut_tree_age_groups
districts / cut_tree_age_groups_with_predictions
districts / object_type
```

### suburbs
Aggregations collected under suburbs within city districts. To contextualize subursb and districs, refer to endpoint:    
meta / suburbs_districts    

```
suburbs / tree_count
suburbs / cut_tree_count
suburbs / genus
suburbs / genus_with_predictions
suburbs / cut_tree_genus
suburbs / cut_tree_genus_with_predictions
suburbs / age_groups
suburbs / age_groups_with_predictions
suburbs / cut_tree_age_groups
suburbs / cut_tree_age_groups_with_predictions
suburbs / object_type
```

### genus
Aggregations collected under the genus of a tree. ("age_groups_with_prediction" uses predictions on both genus and agegroups.)    

```
genus / tree_count
genus / tree_count_with_prediction
genus / cut_tree_count
genus / cut_tree_count_with_prediction
genus / district
genus / district_with_prediction
genus / age_groups
genus / age_groups_with_prediction
genus / ground_truth_bole_radius_year_planting
genus / regression_bole_radius_year_sprout
```

### meta
Usefull meta-information to contextualize requests of different endpoint groups.    

```
meta / districts_suburbs
meta / suburbs_districts
meta / genus_name_german
meta / name_german_genus
meta / genus_species_name_german
meta / species_name_german
meta / species_name_german_genus
meta / species_name_german_species
meta / taxonomy
meta / district_data_completeness
meta / suburb_data_completeness
meta / data_completeness
meta / overall_tree_count
```


### objects_type
Aggregations collected under object types (tree environment) where a tree is located. The object types are defined as followed: 
- allotment garden
- sports field
- playground
- building/school/dormitory (home) building
- street/court (plaza)
- green space
- cemetery
- biotope area
- river/creek
- special facility
- forest
- compensatory area

or "unknown"

```
object_type / tree_count
object_type / cut_tree_count
object_type / district
object_type / suburb
object_type / age_groups
object_type / age_groups_with_prediction
object_type / ground_truth_bole_radius_year_planting
object_type / regression_bole_radius_year_sprout
```

The data source is the official tree inventory.


### location_type
Aggregations collected under location types (tree environment) where a tree is located.

```
location_type / tree_count_location_type
location_type / cut_tree_count_location_type
location_type / tree_count_osm_keys
location_type / cut_tree_count_osm_keys
```

The data source is a match of the tree (point) location with OpenStreetMap (OSM) data.