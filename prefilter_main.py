from prefilter_conf import (
    estc_csv_location,
    sane_out,
    false_out,
    duplicated_out,
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
                         sane_buffer,
                         filter_buffer,
                         duplicated_buffer,
                         force_write=False):

    new_estc_entry = ESTCMARCEntry(record_lines)

    if new_estc_entry.testrecord or not new_estc_entry.curives_sane:
        filter_buffer.add_marc_entry(new_estc_entry)
    elif new_estc_entry.curives in processed_curives:
        duplicated_buffer.add_marc_entry(new_estc_entry)
    else:
        sane_buffer.add_marc_entry(new_estc_entry)

    if force_write:
        sane_buffer.write_marc_entry_csv()
        filter_buffer.write_marc_entry_csv()
        duplicated_buffer.write_marc_entry_csv()

    return new_estc_entry.curives


# ------------------------------------------
# Main script
# ------------------------------------------

# !OBS Input and output location in ./prefilter_conf.py .

# Setup output write buffers.
sane_estc_entry_buffer = ESTCMARCEntryWriteBuffer(sane_out)
filter_estc_entry_buffer = ESTCMARCEntryWriteBuffer(false_out)
duplicated_estc_entry_buffer = ESTCMARCEntryWriteBuffer(duplicated_out)


# Loop all lines in raw ESTC csv.
# Process each record, write outputs now and then.
prev_record_seq = None
record_lines = list()
processed_curives = list()


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

        processed_id = process_record_lines(
            record_lines,
            sane_estc_entry_buffer,
            filter_estc_entry_buffer,
            duplicated_estc_entry_buffer)

        processed_curives.append(processed_id)
        record_lines = [row]
        prev_record_seq = current_record_seq
    # If record seq does not change, append to working record buffer.
    else:
        record_lines.append(row)

# Process last lines left in read buffer and write stuff left in write buffers:
process_record_lines(
    record_lines,
    sane_estc_entry_buffer,
    filter_estc_entry_buffer,
    duplicated_estc_entry_buffer,
    force_write=True)

print("")
print("Done!")

print("Writing summaryfile ...")
create_prefilter_summary_file(estc_csv_location,
                              sane_out,
                              false_out,
                              duplicated_out,
                              summaryfile_location)
print("Done!")
