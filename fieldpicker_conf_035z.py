# -----------------------
# Input conf
# -----------------------
# ESTC input csv location
estc_csv = "out/estc_raw_sane.csv"

# -----------------------
# Output conf
# -----------------------
# Only these fields (and subfields) will be preserved in the output.
# If subfield is omitted all subfields will be kept.
# Also, if subfield has the value 'all', all subfields will be kept.
# If you want to have multiple subfields, but not all for a particular field,
# add an entry for each combination.
fields_keep = [{'field': '035', 'subfield': 'z'}]

fields_outfile = "./out/fields_picked_035z.csv"
