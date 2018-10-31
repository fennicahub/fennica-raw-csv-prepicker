# Field names in the csvs (input and output):
# Record_seq, Field_seq, Subfield_seq, Field_code, Subfield_code, Value
# Input and output tab-separated csv.

# -------------------
# Input files
# -------------------
estc_csv_location = "../estc-data-private/estc-csv-raw/estc-raw.csv"

# -------------------
# Output files
# -------------------
# Valid entries
sane_out = "./out/estc_raw_sane.csv"
# Entries with missing or invalid id or detected as test entries
false_out = "./out/estc_raw_bad.csv"
# Entries with id that has already been processed
duplicated_out = "./out/estc_raw_duplicated.csv"

summaryfile_location = "./out/summary.md"
