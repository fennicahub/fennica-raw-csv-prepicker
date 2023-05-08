import argparse

from lib.fennica_prepicker_common import (
    get_file_len,
    print_progress,
    read_fennica_csv,
    )

from lib.config_reader import get_json_conf

from lib.fennica_marc import (
    fennicaMARCEntry,
    fennicaMARCEntryWriteBuffer)


def process_record_lines(record_lines,
                         fields_to_pick,
                         output_buffer,
                         force_write=False):
    new_fennica_entry = fennicaMARCEntry(record_lines)
    new_fennica_entry.keep_fields(fields_to_pick)
    output_buffer.add_marc_entry(new_fennica_entry)
    if force_write:
        output_buffer.write_marc_entry_csv()


if __name__ == "__main__":

    # get config file location
    parser = argparse.ArgumentParser(
        description="Fieldpicker for (full) fennica csv.")
    parser.add_argument("--conf", help="Location of configuration file",
                        required=True)
    args = parser.parse_args()

    confdata = get_json_conf(args.conf)
    fennica_csv = confdata['fennica_csv']
    fields_keep = confdata['fields_keep']
    fields_outfile = confdata['fields_outfile']

    prev_record_seq = None
    record_lines = list()
    output_buffer = fennicaMARCEntryWriteBuffer(fields_outfile)

    i = 0
    file_lines = get_file_len(fennica_csv)

    print("Picking fields ...")
    for row in read_fennica_csv(fennica_csv):

        i += 1
        if i % 1000 == 0:
            print_progress(i, file_lines)

        if prev_record_seq is None:
            prev_record_seq = row.get('Record_seq')
        current_record_seq = row.get('Record_seq')
        # Check if Record_seq changes. If changed, process record and start new

        if current_record_seq != prev_record_seq:
            process_record_lines(
                record_lines,
                fields_keep,
                output_buffer)
            record_lines = [row]
            prev_record_seq = current_record_seq
        # If record seq does not change, append to working record buffer.
        else:
            record_lines.append(row)

    process_record_lines(
        record_lines,
        fields_keep,
        output_buffer,
        force_write=True)
