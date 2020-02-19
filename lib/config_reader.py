import json
import sys


def get_json_conf(json_fname):
    with open("cfg/" + json_fname) as json_file:
        data = json.load(json_file)
        req_keys = {'fields_keep', 'estc_csv', 'fields_outfile'}
        if req_keys.intersection(set(data.keys())) != req_keys:
            sys.exit("ERROR. Config file keys must contain:" +
                     " 'fields_keep', 'estc_csv', 'fields_outfile'.")
        return data
