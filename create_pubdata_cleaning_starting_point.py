import csv

from lib.estc_prepicker_common import (
    get_file_len,
    print_progress,
    read_estc_csv
    )

from fieldpicker_conf import (
    estc_csv
    )

from lib.estc_marc import (
    ESTCMARCEntry
    )


def get_record_lines_pubdata(record_lines):
    new_estc_entry = ESTCMARCEntry(record_lines)
    pubdata = new_estc_entry.get_pubdata()
    return pubdata


prev_record_seq = None
record_lines = list()
output_file = "out/publisher_data_raw.csv"


i = 0
file_lines = get_file_len(estc_csv)

all_pub_entries = []
print("Pubdata test")
for row in read_estc_csv(estc_csv):

    i += 1
    if i % 1000 == 0:
        print_progress(i, file_lines)

    if prev_record_seq is None:
        prev_record_seq = row.get('Record_seq')
    current_record_seq = row.get('Record_seq')
    # Check if Record_seq changes. If changed, process record and start new

    if current_record_seq != prev_record_seq:
        pub_entries = get_record_lines_pubdata(record_lines)
        for pub_entry in pub_entries:
            all_pub_entries.append(pub_entry)
        record_lines = [row]
        prev_record_seq = current_record_seq
    # If record seq does not change, append to working record buffer.
    else:
        record_lines.append(row)

pub_entries = get_record_lines_pubdata(record_lines)
for pub_entry in pub_entries:
    all_pub_entries.append(pub_entry)


with open(output_file, 'w') as outcsv:
    fieldnames = ['cu-rives', '260_pub_loc', '260_pub_statement',
                  '260_pub_time']
    writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_pub_entries:
        writer.writerow(row)
