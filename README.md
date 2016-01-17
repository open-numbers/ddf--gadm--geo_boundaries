## Data
This dataset contains geographic boundaries of subdivisions of countries, mainly from [GADM][GADM], which is a spatial database of the location of the world's administrative areas (or adminstrative boundaries) for use in GIS and similar software. See [GADM][GADM] for more info about the underlaying data and the coverage. Currently nothing but the intention is to inclde the majority of content that [GADM][GADM] has.

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
