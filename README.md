This dataset contains geographic boundaries of subdivisions of countries.

Most of the data comes from [GADM][GADM], which is a spatial database of the location of the world's administrative areas (or adminstrative boundaries) for use in GIS and similar software. This is work in progress. We intend to keep all gadm subdivisions in ddf format. See [GADM] for more info.

## Dataset scope
Currently nothing.

## How to update
### Step 1. Run ETL Script
#### Requirements
Install python pandas (as described in [pandas][pandas])

#### Run

    python etl/process.py

### Step 2. Edit manual files

## License
[Creative Common Attribution 4.0 International][CC]

[CC]: https://creativecommons.org/licenses/by/4.0/
[GADM]:  http://www.gadm.org/
[pandas]: http://www.gadm.org/
