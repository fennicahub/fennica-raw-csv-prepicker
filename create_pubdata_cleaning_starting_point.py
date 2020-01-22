import csv

from lib.estc_prepicker_common import (
    get_file_len,
    print_progress,
    read_estc_csv,
    get_record_id_curives_pairs
    )

from fieldpicker_conf import (
    estc_csv
    )

from lib.estc_marc import (
    ESTCMARCEntry
    )


def update_pub_out(record_lines, valid_pub_entries, record_seq_sane_set):
    new_estc_entry = ESTCMARCEntry(record_lines)
    if new_estc_entry.record_seq in record_seq_sane_set:
        pub_entries = new_estc_entry.get_pubdata()
        for pub_entry in pub_entries:
            valid_pub_entries.append(pub_entry)
    return valid_pub_entries


def get_sane_record_seqs(record_id_curives_pairs):
    record_seq_sane = set()
    for item in record_id_curives_pairs:
        if item['category'] == "sane":
            record_seq_sane.add(item['record_seq'])
    return record_seq_sane


prev_record_seq = None
record_lines = list()
output_file = "out/publisher_data_raw.csv"
recid_curives_csv = (
    "../estc-data-verified/estc-csv-raw-filtered/record_id_curives_pairs.csv")
record_id_curives_pairs = get_record_id_curives_pairs(recid_curives_csv)
record_seq_sane_set = get_sane_record_seqs(record_id_curives_pairs)

# count number of lines to be processed for counter
i = 0
file_lines = get_file_len(estc_csv)

# Process input
all_pub_entries = []
for row in read_estc_csv(estc_csv):

    i += 1
    if i % 1000 == 0:
        print_progress(i, file_lines)

    if prev_record_seq is None:
        prev_record_seq = row.get('Record_seq')
    current_record_seq = row.get('Record_seq')
    # Check if Record_seq changes. If changed, process record and start new

    if current_record_seq != prev_record_seq:
        all_pub_entries = update_pub_out(
            record_lines, all_pub_entries, record_seq_sane_set)
        record_lines = [row]
        prev_record_seq = current_record_seq
    # If record seq does not change, append to working record buffer.
    else:
        record_lines.append(row)

all_pub_entries = update_pub_out(
    record_lines, all_pub_entries, record_seq_sane_set)


# Write final output.
with open(output_file, 'w') as outcsv:
    fieldnames = ['cu-rives', '260_pub_loc', '260_pub_statement',
                  '260_pub_time']
    writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_pub_entries:
        writer.writerow(row)
