import csv


def get_file_len(filename):
    with open(filename, 'r', encoding="utf-8") as countfile:
        for i, l in enumerate(countfile):
            pass
        return i + 1


def print_progress(current_i, max_i):
    percentage_str = str(round(current_i / float(max_i) * 100, 1)) + "%"
    print("Progress: " + percentage_str,
          end="\r", flush=True)


def read_estc_csv(estc_csv_location):
    with open(estc_csv_location, "r", encoding="utf-8") as csvfile:
        datareader = csv.DictReader(csvfile, delimiter="\t")
        for row in datareader:
            yield row
