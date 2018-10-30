# Field names in the csvs (input and output):
# Record_seq, Field_seq, Subfield_seq, Field_code, Subfield_code, Value
# Input and output tab-separated csv.

# -------------------
# Input files
# -------------------
estc_csv_location = "./data-temp/estc.csv"

# -------------------
# Output files
# -------------------
# Valid entries
sane_out = "./out-test/sane.csv"
# Entries missing an id or detected as test entries
false_out = "./out-test/false.csv"
# Entries with id that has already been processed
duplicated_out = "./out-test/duplicated.csv"
