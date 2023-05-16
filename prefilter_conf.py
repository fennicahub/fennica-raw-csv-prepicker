# Field names in the csvs (input and output):
# record_number (Record_seq), field_number(Field_seq), subfield_number(Subfield_seq), field_code(Field_code), subfield_code(Subfield_code), value(Value)
# Input and output tab-separated csv.

# -------------------
# Input files
# -------------------
fennica_csv_location = "/home/ubuntu/git/full.csv"
# testset:
# fennica_csv_location = "data-temp/sample1-10000.csv"

# -------------------
# Output files
# -------------------
# Valid entries
sane_out = "./out/fennica_raw_sane.csv"
# Entries with missing or invalid id or detected as test entries
false_out = "./out/fennica_raw_bad.csv"
# Entries with id that has already been processed
duplicated_out = "./out/fennica_raw_duplicated.csv"
# Table with record sequence and fennica_id pairs
rec_id_table_output_location = "./out/record_seq_fennica_id_pairs.csv"
# Final fennica unification input data table

summaryfile_location = "./out/summary.md"
