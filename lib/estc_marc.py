import csv
import os


class ESTCMARCEntry(object):
    def __init__(self, data_lines, curives_filterset=None):
        self.data_lines = data_lines
        self.curives = self.find_curives(curives_filterset)
        self.testrecord = self.is_test_record()
        self.curives_sane = self.test_curives(self.curives, curives_filterset)
        self.record_seq = self.get_rec_seq()
        self.estc_id = self.get_estc_id()

    def find_curives(self, curives_filterset=None):
        curives_candidates = []
        for line in self.data_lines:
            if (line['Field_code'] == "035" and
                    line['Subfield_code'] == "a"):
                curives_candidates.append(line['Value'])
        good_candidates = []
        for curives_candidate in curives_candidates:
            is_good_candidate = self.test_curives(curives_candidate,
                                                  curives_filterset)
            if is_good_candidate:
                good_candidates.append(curives_candidate)
        if len(good_candidates) == 0:
            curives = None
        else:
            curives = good_candidates[0]
        return curives

    def test_data_lines(self):
        prev_rec_seq = None
        for line in self.data_lines:
            rec_seq = line['Record_seq']
            if prev_rec_seq is None:
                prev_rec_seq = rec_seq
            elif prev_rec_seq != rec_seq:
                print("Record seq mismatch!")
                print("curives: " + self.curives)
                print("req_sec_prev: " + prev_rec_seq)
                print("req_sec_new: " + rec_seq)
                return False
        return True

    def get_rec_seq(self):
        rec_seq = self.data_lines[0]['Record_seq']
        return rec_seq

    def get_lines(self):
        return self.data_lines

    def get_estc_id(self):
        if self.curives is not None:
            return self.curives.split('(CU-RivES)')[-1]
        else:
            return None

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

    def test_curives(self, curives_value, curives_filterset=None):
        if curives_value is None:
            return False
        if curives_value == "":
            return False
        if curives_value == "(CU-RivES)":
            return False
        if len(curives_value) < 11:
            return False
        if curives_value[0:10] != "(CU-RivES)":
            return False
        if curives_filterset is not None:
            if curives_value in curives_filterset:
                return False
        return True

    def get_filtered_fields(self, fields_list):
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

        return filtered_data_lines

    def keep_fields(self, fields_list):
        self.data_lines = self.get_filtered_fields(fields_list)

    def get_pubdata(self):
        pubfields = self.get_filtered_fields(
            [{'field': '260', 'subfield': 'all'}])

        pubdata_list = []

        for row in pubfields:

            create_new_row = False

            if row['Subfield_code'] == 'a' or row['Subfield_code'] == 'e':
                row_type = 'pub_loc_raw'
                create_new_row = True
            elif row['Subfield_code'] == 'b' or row['Subfield_code'] == 'f':
                row_type = 'pub_statement_raw'
            elif row['Subfield_code'] == 'c' or row['Subfield_code'] == 'g':
                row_type = 'pub_time_raw'
            else:
                print("Unexpected subfield:")
                print(row)
                print("\n")
                continue

            # if previous entry already has value in field type, create new
            # if current row is location, create new
            if len(pubdata_list) == 0:
                create_new_row = True
            elif pubdata_list[-1].get(row_type) is not None:
                create_new_row = True
            elif row_type == 'pub_loc_raw':
                create_new_row = True

            # if new rows are not created, update all previous rows missing
            # info in current subfield with the subfield contents
            if not create_new_row:
                for pubdata_dict in pubdata_list:
                    if pubdata_dict[row_type] is None:
                        pubdata_dict[row_type] = row['Value']

            # if new_row flag set, create the new row.
            if create_new_row:
                new_pubdata_outrow = {'cu_rives': self.curives,
                                      'pub_loc_raw': None,
                                      'pub_statement_raw': None,
                                      'pub_time_raw': None}
                new_pubdata_outrow[row_type] = row['Value']
                pubdata_list.append(new_pubdata_outrow)

        return pubdata_list


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

        header_row = ['estc_id', 'Record_seq', 'Field_seq', 'Subfield_seq',
                      'Field_code', 'Subfield_code', 'Value']

        with open(self.csv_file, write_method,
                  encoding='utf-8') as csv_outfile:

            csvwriter = csv.writer(csv_outfile, delimiter='\t')
            if write_header:
                csvwriter.writerow(header_row)
            for MARC_entry in self.MARC_entry_list:
                for line in MARC_entry.data_lines:
                    csvwriter.writerow([
                        MARC_entry.estc_id,
                        line.get('Record_seq'),
                        line.get('Field_seq'),
                        line.get('Subfield_seq'),
                        line.get('Field_code'),
                        line.get('Subfield_code'),
                        line.get('Value')])

        if flush_buffer:
            self.MARC_entry_list = list()
