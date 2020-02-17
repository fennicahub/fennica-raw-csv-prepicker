# Field names in the csvs (input and output):
# Record_seq, Field_seq, Subfield_seq, Field_code, Subfield_code, Value
# Input and output tab-separated csv.

# -------------------
# Input files
# -------------------
estc_csv_location = "../estc-data-originals/estc-csv-raw/estc_raw.csv"
# testset:
# estc_csv_location = "data-temp/sample1-10000.csv"

# -------------------
# Output files
# -------------------
# Valid entries
sane_out = "./out/estc_raw_sane.csv"
# Entries with missing or invalid id or detected as test entries
false_out = "./out/estc_raw_bad.csv"
# Entries with id that has already been processed
duplicated_out = "./out/estc_raw_duplicated.csv"
# Table with record sequence and estc_id pairs
rec_id_table_output_location = "./out/record_seq_estc_id_pairs.csv"
# Final ESTC unification input data table

summaryfile_location = "./out/summary.md"
