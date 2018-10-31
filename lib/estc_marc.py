import csv
import os


class ESTCMARCEntry(object):
    def __init__(self, data_lines):
        self.data_lines = data_lines
        self.curives = self.find_curives()
        self.testrecord = self.is_test_record()
        self.curives_sane = self.sane_curives()

    def find_curives(self):
        curives = None
        for line in self.data_lines:
            if (line['Field_code'] == "035" and
                    line['Subfield_code'] == "a"):
                curives = line['Value']
                # print(curives)
                break
        return curives

    def get_lines(self):
        return self.data_lines

    def is_test_record(self):
        test_lower = [
            "please ignore",
            "test record",
            "be deleted",
            "to delete",
            "download",
            "test test"]
        test_exact = [
            "DO NOT MATCH",
            "GHOST",
            "RECORD DELETED"
        ]
        for line in self.data_lines:
            line_value = line['Value']
            if line_value is None:
                continue
            for test_case in test_lower:
                if line_value.lower().find(test_case) != -1:
                    return True
            for test_case in test_exact:
                if line_value.find(test_case) != -1:
                    return True
        return False

    def sane_curives(self):
        if self.curives is None:
            return False
        if self.curives == "":
            return False
        if self.curives == "(CU-RivES)":
            return False
        return True

    def keep_fields(self, fields_list):
        filtered_data_lines = list()
        for line in self.data_lines:

            if (line.get('Value') is None or
                    line.get('Value') == ""):
                continue

            for filter_field in fields_list:
                if line.get('Field_code') == filter_field.get('field'):
                    if (filter_field.get('subfield') == 'all' or
                            filter_field.get('subfield') is None):
                        filtered_data_lines.append(line)
                    elif (filter_field.get('subfield') ==
                            line.get('Subfield_code')):
                        filtered_data_lines.append(line)

        self.data_lines = filtered_data_lines


class ESTCMARCEntryWriteBuffer(object):
    def __init__(self, csv_file):
        self.MARC_entry_list = list()
        self.csv_file = csv_file

    def add_marc_entry(self, MARC_entry):
        self.MARC_entry_list.append(MARC_entry)
        if len(self.MARC_entry_list) == 10000:
            self.write_marc_entry_csv()

    def write_marc_entry_csv(self, append=True, flush_buffer=True):
        if append:
            write_method = 'a'
        else:
            write_method = 'w'

        if os.path.exists(self.csv_file):
            write_header = False
        else:
            write_header = True

        header_row = ['Record_seq', 'Field_seq', 'Subfield_seq',
                      'Field_code', 'Subfield_code', 'Value']

        with open(self.csv_file, write_method,
                  encoding='utf-8') as csv_outfile:

            csvwriter = csv.writer(csv_outfile, delimiter='\t')
            if write_header:
                csvwriter.writerow(header_row)
            for MARC_entry in self.MARC_entry_list:
                for line in MARC_entry.data_lines:
                    csvwriter.writerow([
                        line.get('Record_seq'),
                        line.get('Field_seq'),
                        line.get('Subfield_seq'),
                        line.get('Field_code'),
                        line.get('Subfield_code'),
                        line.get('Value')])

        if flush_buffer:
            self.MARC_entry_list = list()
