# ESTC raw csv prepicker

This is a package of two scripts for filtering the raw parsed ESTC csv.

[ESTC raw csv precleaner]("estc-raw-csv-precleaner") allows filtering erroneous and duplicated data to the raw csv and outputting filtered data in the save csv format.

[ESTC csv fieldpicker]("estc-csv-fieldpicker") allows subsetting the csv and picking selected fields for further analysis. It maintains the same csv format, but only keeps selected fields (with value) and associated Cu-Rives numbers.

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

**OBS!** The script was developed and tested with Python 3.6. Who knows what might happen with another version! No additional libraries needed.

1) Set input and output file locations in `prefilter_conf.py`.
2) Run `prefilter_main.py`.

## ESTC csv fieldpicker

**To be done!**
