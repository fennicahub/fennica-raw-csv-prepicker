# Fennica raw csv prepicker

See [change log](change.log)

This is a package of two scripts for filtering the raw parsed Fennica csv.

**OBS!** The scripts were developed and tested with **Python 3.6**. No additional libraries needed.

[Fennica raw csv precleaner](#fennica-raw-csv-precleaner) allows filtering erroneous and duplicated data to the raw csv and outputting filtered data in the save csv format.

[Fennica csv fieldpicker](#fennica-csv-fieldpicker) allows subsetting the csv and picking selected fields for further analysis. It maintains the same csv format, but only keeps selected fields (with value) and associated ID numbers.

[Pubdata cleanup starting data](#pubdata-cleanup-starting-data) creates a csv in a different format that plugs into the start of the publisher data cleanup script. That one employs a custom method in **FennicaMARCEntry** -class in [fennica_marc.py](./lib/fennica_marc.py) and serves as an example of creating a starting data subset for a cleanup script. The MARC format for the different fields varies, so creating an universal function for this task doe not seem feasible.


## Fennica raw csv precleaner

The purpose of this script is to allow filtering the raw Fennica csv. It removes various test records and and other garbage left in the csv. It makes sure that there are no duplicated IDs, and no entries that are missing and id. All the filtered entries are output to separate csv files to allow manual inpection.

### Input

* Raw [Fennica .csv -file](https://github.com/fennicahub/fennica-data-originals/tree/master/fennica-csv-raw) produced by **[fennicahub/fennica-xml2csv](https://github.com/fennicahub/fennica-xml2csv)** from input data at  [fennicahub/fennica-data-originals](https://github.com/fennicahub/fennica-data-originals/tree/master/fennica-xml-raw).

### Output

Output is csv with rows separated by **tabs**.

The script produces 3 output files (with file names configured in `./prefilter_conf.py`):
* "Sane" Fennica entries. **This is the one you want for starting point of cleaning scripts. Nothing else needed.** 
* Erroneous entries filtered out.
* Duplicated entries also filtered out.

There's also a separate table only containing the record_seq and fennica_id mappings and sanity status. 

### Running the script

1) Set input and output file locations in `prefilter_conf.py` (symbolic links can help to avoid user specific paths)
2) Run `prefilter_main.py` (e.g. `python3 prefilter_main.py`); see `prefilter_conf.py` for the file paths
3) Use [copy.sh](copy.sh) to Copy the files from out/ into github repository: [fennicahub/fennica-data-verified/fennica-csv-raw-filtered/](https://github.com/fennicahub/fennica-data-verified/tree/master/fennica-csv-raw-filtered); remember to push the updates
 
## Fennica csv fieldpicker: **fieldpicker.py**

An Fennica fieldpicker that even your grandma could use. Allows you to filter the big Fennica csv and only keep the fields that are needed for your processing pipeline.

### Input

Fennica csv in the same format as for the above script. Preferably one that has already been filtered for duplicates, etc. In practically all cases this should be **fennica_raw_sane.csv** found here: [fennicahub/fennica-data-verified/fennica-csv-raw-filtered/](https://github.com/fennicahub/fennica-data-verified/tree/master/fennica-csv-raw-filtered).

### Output

Output is in the same format as the input, with only the user specified fields remaining.

### Running the script

1) Create a config json file in `./cfg/` subdirectory. See for example `pub260.json`.
2) Run `fieldpicker.py --conf [yourconf_file]` (e.g. `python fieldpicker.py --conf pub260.json`)



# Further utilities for specific fields

## Pubdata cleanup starting data

The script is at [create_pubdata_cleaning_starting_point.py](./create_pubdata_cleaning_starting_point.py). Configuration variables are set within the script file.

### Input

Takes the output of either of the above scripts as input. Input should include all the information for MARC field 260.

### Output

Creates a `.csv` table like this as output at the location set in the script file:

| cu-rives | 260_pub_loc | 260_pub_statement | 260_pub_time |
| -------- | ----------- | ----------------- | ------------ |
| (CU-RivES)N30954 | Basil : | Printed by J.J. Tourneisen ; | MDCCLXXXIX. [1789] |
| (CU-RivES)N30954 | Paris : | "Sold by Pissot, bookseller, Quai des Augustins," | MDCCLXXXIX. [1789] |
| ... | ... | ... | ... |


### Acknowledgments

This script has been derived from the original code by Ville Vaara at
[https://github.com/COMHIS/fennica-raw-csv-prepicker]