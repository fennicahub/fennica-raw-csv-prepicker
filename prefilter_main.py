import csv

from prefilter_conf import (
    estc_csv_location,
    sane_out,
    false_out,
    duplicated_out,
    rec_id_table_output_location,
    summaryfile_location
    )

from lib.estc_marc import (
    ESTCMARCEntry,
    ESTCMARCEntryWriteBuffer)

from lib.estc_prepicker_common import (
    get_file_len,
    print_progress,
    read_estc_csv,
    create_prefilter_summary_file
    )


def process_record_lines(record_lines,
                         processed_entries,
                         sane_buffer,
                         filter_buffer,
                         duplicated_buffer,
                         filterid_set=None,
                         force_write=False):

    new_estc_entry = ESTCMARCEntry(record_lines, filterid_set)

    if new_estc_entry.testrecord or not new_estc_entry.curives_sane:
        master_record_list.append(new_estc_entry.record_seq)
        filter_buffer.add_marc_entry(new_estc_entry)
        processed_entries['category'].append("bad")
    elif new_estc_entry.curives in processed_entries['estc_id']:
        duplicated_buffer.add_marc_entry(new_estc_entry)
        processed_entries['category'].append("duplicated")
    else:
        sane_buffer.add_marc_entry(new_estc_entry)
        processed_entries['category'].append("sane")

    processed_entries['record_seq'].append(new_estc_entry.record_seq)
    processed_entries['estc_id'].append(new_estc_entry.curives)

    if force_write:
        sane_buffer.write_marc_entry_csv()
        filter_buffer.write_marc_entry_csv()
        duplicated_buffer.write_marc_entry_csv()

    return processed_entries


def load_filterdata_set(filterdata_location):
    with open(filterdata_location, 'r') as csvfile:
        filterlist = []
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            line_split = line[0].split('(')
            for item in line_split:
                if len(item) > 0:
                    item = "(" + item
                    filterlist.append(item)
        filterset = set(filterlist)
        return filterset


def write_rec_id_table(processed_entries, output_location):
    with open(output_location, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['record_seq', 'estc_id', 'category'])
        for i in range(0, len(processed_entries['record_seq'])):
            csvwriter.writerow([processed_entries['record_seq'][i],
                                processed_entries['estc_id'][i],
                                processed_entries['category'][i]])


def get_035z_values(estc_raw_csv):
    values_035z = []
    with open(estc_raw_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='\t')
        for row in csvreader:
            if row['Field_code'] == '035' and row['Subfield_code'] == "z":
                this_items = row['Value'].lower().split("(cu-rives)")
                for item in this_items:
                    item_u = item.upper()
                    if len(item_u) > 0:
                        values_035z.append(item_u)
    return set(values_035z)


# ------------------------------------------
# Main script
# ------------------------------------------

# !OBS Input and output location in ./prefilter_conf.py .

# generate filterdata:
print("Getting values in 035z for filtering bad ids ...")
filterid_set = get_035z_values(estc_csv_location)
print("   ... done!")

# Setup output write buffers.
sane_estc_entry_buffer = ESTCMARCEntryWriteBuffer(sane_out)
filter_estc_entry_buffer = ESTCMARCEntryWriteBuffer(false_out)
duplicated_estc_entry_buffer = ESTCMARCEntryWriteBuffer(duplicated_out)
master_record_list = []

# Loop all lines in raw ESTC csv.
# Process each record, write outputs now and then.
prev_record_seq = None
record_lines = list()
# processed_curives = list()
processed_entries = {'record_seq': [],
                     'estc_id': [],
                     'category': []}

file_lines = get_file_len(estc_csv_location)
# Process each record line (and create marc entry)
i = 0
print("Processing ESTC csv ...")

for row in read_estc_csv(estc_csv_location):

    i += 1
    if i % 1000 == 0:
        print_progress(i, file_lines)

    # Special case for first entry
    if prev_record_seq is None:
        prev_record_seq = row.get('Record_seq')
    current_record_seq = row.get('Record_seq')

    # Check if Record_seq changes. If changed, process record and start new
    if current_record_seq != prev_record_seq:
        processed_entries = process_record_lines(
            record_lines,
            processed_entries,
            sane_estc_entry_buffer,
            filter_estc_entry_buffer,
            duplicated_estc_entry_buffer,
            filterid_set=filterid_set)
        # processed_curives.append(processed_id_pair['curives'])
        record_lines = [row]
        prev_record_seq = current_record_seq
    # If record seq does not change, append to working record buffer.
    else:
        record_lines.append(row)

# Process last lines left in read buffer and write stuff left in write buffers:
processed_entries = process_record_lines(
    record_lines,
    processed_entries,
    sane_estc_entry_buffer,
    filter_estc_entry_buffer,
    duplicated_estc_entry_buffer,
    filterid_set=filterid_set,
    force_write=True)

print("")
print("Done!")

print("Writing record id table ...")
write_rec_id_table(processed_entries, rec_id_table_output_location)
print("")
print("Done!")

print("Writing summaryfile ...")
create_prefilter_summary_file(estc_csv_location,
                              sane_out,
                              false_out,
                              duplicated_out,
                              summaryfile_location)
print("Done!")
