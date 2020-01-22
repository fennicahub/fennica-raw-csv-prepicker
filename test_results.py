import csv

testres = []
with open("out/record_id_curives_pairs.csv", 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        testres.append(row)

sane_ids = []
sane_count = 0
for item in testres:
    if item['category'] == "sane":
        sane_count += 1
        sane_ids.append(item['curives'])
