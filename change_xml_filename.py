from xml.etree import ElementTree as ET
import glob
import os
import cv2


def change_xml_filename(xml_path, out_dir, new_name):
    '''
    改变labelimg标注后xml文件中文件名，同时更改对应图片名。
    :param xml_path: 给出xml所在的路劲
    :return:
    '''
    new_n = new_name + ".png"
    ############# 更改相应图片的名字 #################
    exts = [".jpg", ".jpeg", ".png", ".bmp"]
    for ext in exts:
        img_dir = xml_path.split(".")[0] + ext
        if os.path.isfile(img_dir):
            img = cv2.imread(img_dir)
            cv2.imwrite(os.path.join(out_dir, new_n), img)

    ############# 更该对应xml文件中的图片名和路劲 #############
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for node in root:
        if node.tag == "filename":
            # print(node.tag, ": ", node.text)
            node.text = new_n
        if node.tag == "path":
            # print(node.tag, ": ", node.text)
            node.text = os.path.join(out_dir, new_n)

    tree.write(os.path.join(out_dir, new_name + ".xml"), encoding="utf-8")


if __name__ == "__main__":
    file_path = "/home/dp/Documents/datasets/guan_gan/img/1"
    out_dir = "/home/dp/Documents/datasets/guan_gan/img/totals"
    files = glob.glob(file_path + "/*.xml") ###输入xml完整路劲
    for file in files:
        filename = file.split("/")[-1].split(".")[0]
        filename = "1_" + filename
        print(file)
        change_xml_filename(file, out_dir, filename)

    print("done!!!")