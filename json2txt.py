import json

file = "/home/dp/Documents/datasets1/all_files/annotations/train_qx.json"
with open(file, "r", encoding='utf-8') as f:
    files = json.load(f)
imgs_ids = []
imgs_bboxes = {}
for img in files["images"]:
    bboxes = []
    for anno in files["annotations"]:
        file_name = img["file_name"]
        id = img["id"]

        img_id = anno["image_id"]
        bbox = anno["bbox"]

        if id == img_id:
            bboxes.append(bbox)
    imgs_bboxes[file_name] = bboxes

for img_bboxes in imgs_bboxes.items():

    file_name = img_bboxes[0]
    bboxes = img_bboxes[1]
    print(file_name)
    print(bboxes)
    f = open("train.txt", "+a")
    f.write(str(file_name) + ' ' + str(bboxes) + '\n')
f.close()