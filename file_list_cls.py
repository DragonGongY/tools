import os

file_path = "/media/dp/文档/tools/6"
f = open("mot.train", 'w')
for file in os.listdir(file_path):
    if file.endswith("xml"):
        continue
    txt = str(6) + '/' + file + " " + '\n'
    f.write(txt)
f.close()