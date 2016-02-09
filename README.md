## Data
This dataset contains geographic boundaries of subdivisions of countries, mainly from [GADM][GADM], which is a spatial database of the location of the world's administrative areas (or adminstrative boundaries) for use in GIS and similar software. See [GADM][GADM] for more info about the underlaying data and the coverage. Currently nothing but the intention is to inclde the majority of content that [GADM][GADM] has.

## Dataset structure
The file ddf--entity_sets.csv, enumerates all geographic subdvisions(Like US-States) found in Gadm. Each subdivision have the following properties as columns in this file:
* id: We generated a unique identifier of the subdivision by concatinating the country id, and the name of the subdivision. for example usa_state.
* name: A singular name that contains the full path including the country: "USA State"
* drilldown_name: A name excluding the country: For example "State"
* country: the id of the country For example "usa"


## How to update
### Step 1. Run ETL Script
#### Requirements
Install python pandas (as described in [ETL Script Requirements][etl_req])

#### Run

    $cd ../process/etl/
    $python partial_etl.py

As the script name indicates, additional etl is done manually.

### Step 2. Edit manual files

## License
Gapmidner created this dataset and provides it under [Creative Common Attribution 4.0 International][CC].

[CC]: https://creativecommons.org/licenses/by/4.0/
[GADM]:  http://www.gadm.org/
[etl_req]: https://github.com/open-numbers/py-scripts/wiki/Python-ETL-Requirements
