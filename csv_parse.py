import csv
import os

csv_path = "/home/dp/Pictures/tools/Video00006.csv"
with open(csv_path) as f:
    row = csv.reader(f)
    height = []
    for r in row:
        file_name = "0" * (8-len(r[0])) + r[0]
        assert len(file_name) == 8
        f = open("/home/dp/Pictures/tools/6/{}.txt".format(file_name), 'w')
        text = r[0] +' '+ r[1]+' ' + r[2]+' ' + r[3]+' ' + r[4]+' ' + r[5]+' ' + r[6]+' ' + r[7]+' ' + r[8]+' ' + r[9]
        f.write(text)

        f.close()

