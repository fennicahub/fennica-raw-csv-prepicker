# ESTC raw csv prepicker

This is a package of two scripts for filtering the raw parsed ESTC csv.

**OBS!** The scripts were developed and tested with **Python 3.6**. Who knows what might happen with another version! Definitely won't be pretty with Python 2.x. No additional libraries needed.

[ESTC raw csv precleaner](#estc-raw-csv-precleaner) allows filtering erroneous and duplicated data to the raw csv and outputting filtered data in the save csv format.

[ESTC csv fieldpicker](#estc-csv-fieldpicker) allows subsetting the csv and picking selected fields for further analysis. It maintains the same csv format, but only keeps selected fields (with value) and associated Cu-Rives numbers.

[Pubdata cleanup starting data](#pubdata-cleanup-starting-data) creates a csv in a different format that plugs into the start of the publisher data cleanup script. That one employs a custom method in **ESTCMARCEntry** -class in [estc_marc.py](./lib/estc_marc.py) and serves as an example of creating a starting data subset for a cleanup script. The MARC format for the different fields varies, so creating an universal function for this task doe not seem feasible.

## ESTC raw csv precleaner

The purpose of this script is to allow filtering the raw ESTC csv. It removes various test records and and other garbage left in the csv. It makes sure that there are no duplicated Cu-Rives ids, and no entries that are missing and id. All the filtered entries are output to separate csv files to allow manual inpection.

### Input

Raw ESTC .csv -file produced by **[COMHIS/estc-xml2csv](https://github.com/COMHIS/estc-xml2csv)**. [COMHIS/estc-data-private/estc-csv-raw](https://github.com/COMHIS/estc-data-private/tree/master/estc-csv-raw).

### Output

Output is csv with rows separated by **tabs**.

The script produces 3 output files (with file names configured in `./prefilter_conf.py`):
* "Sane" ESTC entries.
* Erroneous entries filtered out.
* Duplicated entries also filtered out.

### Running the script

1) Set input and output file locations in `prefilter_conf.py`.
2) Run `prefilter_main.py`.

## ESTC csv fieldpicker

An ESTC fieldpicker that even your grandma could use. Allows you to filter the big ESTC csv and only keep the fields that are needed for your processing pipeline.

### Input

ESTC csv in the same format as for the above script. Preferably one that has already been filtered for duplicates, etc. So, for example estc_raw_sane.csv found here: [COMHIS/estc-data-private/estc-csv-raw-filtered/](https://github.com/COMHIS/estc-data-private/tree/master/estc-csv-raw-filtered).

Additional filter list of ESTC ids used by the script is in [./data-prefilter](./data-prefilter) with a README explaining that data.

### Output

Output is in the same format as the input, with only the user specified fields remaining.

### Running the script

1) Set input and output locations, and the fields you want to keep in the output in `./fieldpicker_conf.py`.
2) Run `fieldpicker_main.py`.

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
