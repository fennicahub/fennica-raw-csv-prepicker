# Field names in the csvs (input and output):
# Record_seq, Field_seq, Subfield_seq, Field_code, Subfield_code, Value
# Input and output tab-separated csv.

# -------------------
# Input files
# -------------------
estc_csv_location = "../estc-data-originals/estc-csv-raw/estc_raw.csv"
# testset:
# estc_csv_location = "data-temp/sample1-10000.csv"
# Below used for filtering out duplicated entries based on values in 035z
filter_data_location = "data-prefilter/field035z-values.csv"

# -------------------
# Output files
# -------------------
# Valid entries
sane_out = "./out/estc_raw_sane.csv"
# Entries with missing or invalid id or detected as test entries
false_out = "./out/estc_raw_bad.csv"
# Entries with id that has already been processed
duplicated_out = "./out/estc_raw_duplicated.csv"

rec_id_table_output_location = "./out/record_id_curives_pairs.csv"

summaryfile_location = "./out/summary.md"
