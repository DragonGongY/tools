import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET

START_BOUNDING_BOX_ID = 1
save_path = "/home/yanglian/Documents/PrePiece_data" 
#"/home/yanglian/Documents/PC_Boards/qx_label"
#save_path = "/home/dp/dataset/qx/annotations"

def get(root, name):
    return root.findall(name)

def get_and_check(root, name, length):
    vars = get(root, name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def convert(xml_list, json_file):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = pre_define_categories.copy()
    bnd_id = START_BOUNDING_BOX_ID
    all_categories = {}
    for index, line in enumerate(xml_list):
        print("Processing %s"%(line))
        xml_f = line
        tree = ET.parse(xml_f)
        root = tree.getroot()
        filename = os.path.basename(xml_f)[:-4] + ".jpg"
        image_id = 20190000001 + index
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width, 'id': image_id}
        json_dict['images'].append(image)
        #  Currently we do not support segmentation
        # segmented = get_and_check(root, 'segmented', 1).text
        # assert segmented == '0'
        print("zhe yi bu is OK 01 !")
        for obj in get(root, 'object'):
            print("zhe yi bu is OK 02 !")
            category = get_and_check(obj, 'name', 1).text
            print("category is:", category)
            print("zhe yi bu is OK 03 !")
            if category in all_categories:
                print("zhe yi bu is OK 04 !")
                all_categories[category] += 1
                print("all_categories is :",all_categories)
            else:
                print("zhe yi bu is OK 05 !")
                all_categories[category] = 1
            '''
            if category not in categories:
                if only_care_pre_define_categories:
                    continue
                new_id = len(categories) + 1
                print( "[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(
                    category, pre_define_categories, new_id))
                categories[category] = new_id     '''
            print("zhe yi bu is OK 06 !")
            category_id = categories[category]
            print("zhe yi bu is OK 07 !")
            bndbox = get_and_check(obj, 'bndbox', 1)
            print("zhe yi bu is OK 08 !")
            xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))
            ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))
            xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
            ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
            assert (xmax > xmin), "xmax <= xmin, {}".format(line)
            assert (ymax > ymin), "ymax <= ymin, {}".format(line)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width * o_height, 'iscrowd': 0, 'image_id': image_id, 'bbox': [xmin, ymin, o_width, o_height], 'category_id': category_id, 'id': bnd_id, 'ignore': 0, 'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'qx', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    print("------------create {} done--------------".format(json_file))
    print("find {} categories: {} -->>> your pre_define_categories {}: {}".format(len(all_categories), all_categories.keys(), len(pre_define_categories), pre_define_categories.keys()))


    print("category: id --> {}".format(categories))
    print(categories.keys())
    print(categories.values())



if __name__ == '__main__':
    # ????????????????????????
    classes = ["LP", "LZ", "SC","MH","ML","MD","WR",'QT']
    for i, cls in enumerate(classes):
        #pre_define_categories[cls] = i + 1
        # ??????????????????????????????id????????????????????????????????????????????????
        pre_define_categories = {"LP":1, "LZ":2, "SC":3,"MH":4,"ML":5,"MD":6,"WR":7,'QT':8}
        only_care_pre_define_categories = True # or False
        # ?????????json??????
        save_json_train = './train_Prepiece.json'
        save_json_val = './val_Preprice.json'
        save_json_test = './test_Preprice.json' # ???????????????????????????
        xml_dir ="/media/dp/LinuxData/DataSets/GuanGan/RJQ/new_label/totals/Annotations"
        xml_list = glob.glob(xml_dir + "/*.xml")
        xml_list = np.sort(xml_list) # ???????????????
        np.random.seed(100)
        np.random.shuffle(xml_list) # ????????????????????????????????????
        train_ratio = 1.0
        val_ratio = 0.1
        train_num = int(len(xml_list) * train_ratio)
        val_num = int(len(xml_list) * val_ratio)
        xml_list_train = xml_list[:train_num]
        xml_list_val = xml_list[train_num: train_num+val_num]
        xml_list_test = xml_list[train_num+val_num:]
        # ???xml????????????coco???????????????????????????????????????json?????????train/test/food???
        convert(xml_list_train, save_json_train)
        convert(xml_list_val, save_json_val)
        convert(xml_list_test, save_json_test)
        # # # ????????????????????????????????????????????? #
        # if os.path.exists(save_path + "/annotations"):
        #     shutil.rmtree(save_path + "/annotations")
        #     os.makedirs(save_path + "/annotations")
        # if os.path.exists(save_path + "/images_divide/train"):
        #     shutil.rmtree(save_path + "/images_divide/train")
        #     os.makedirs(save_path + "/images_divide/train")
        # if os.path.exists(save_path + "/images_divide/val"):
        #     shutil.rmtree(save_path + "/images_divide/val")
        #     os.makedirs(save_path + "/images_divide/val")
        # if os.path.exists(save_path + "/images_divide/test"):
        #     shutil.rmtree(save_path + "/images_divide/test")
        #     os.makedirs(save_path + "/images_divide/test")
        # # # ?????????????????????3???txt????????????????????????????????????
        # f1 = open("./train.txt", "w")
        # for xml in xml_list_train:
        #     img = xml[:-4] + ".jpg"
        #     f1.write(os.path.basename(xml)[:-4] + "\n")
        #     shutil.copyfile(img, save_path + "/images_divide/train/" + os.path.basename(img))
        # f2 = open("val.txt", "w")
        # for xml in xml_list_val:
        #     img = xml[:-4] + ".jpg"
        #     f2.write(os.path.basename(xml)[:-4] + "\n")
        #     shutil.copyfile(img, save_path + "/images_divide/val/" + os.path.basename(img))
        # f3 = open("test.txt", "w")
        # for xml in xml_list_val:
        #     img = xml[:-4] + ".jpg"
        #     f2.write(os.path.basename(xml)[:-4] + "\n")
        #     shutil.copyfile(img, save_path + "/images_divide/test/" + os.path.basename(img))

        # f1.close()
        # f2.close()
        # f3.close()
        print("-" * 50)
        print("train number:", len(xml_list_train))
        print("val number:", len(xml_list_val))
        print("test number:", len(xml_list_val))
