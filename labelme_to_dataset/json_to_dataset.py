#coding:utf-8
import base64
import json
import os
import os.path as osp

import PIL.Image

from color import asgray
from label import label2rgb

import utils

import glob
import cv2

def main(json_file_path, out_dir, label_name_to_value, img_type=".png"):
    """
    Parameters
    ----------
    json_file_path:输入json文件所在的路径，json文件夹下要包含图片。
    out_dir:转换后保存路径.
    label_name_to_value：标签对应的编码，_background_:0
    img_type:图片文件的后缀名
    -------

    """

    for i, json_file in enumerate(glob.glob(os.path.join(json_file_path, "*.json"))):
        print("[INFO] processing {}".format(json_file))

        # img_name = json_file.split("/")[-1].split(".")[0]
        img_name = i
        out_label = os.path.join(out_dir, "Annotations")
        out_img = os.path.join(out_dir, "JPEGImages")

        if not osp.exists(out_dir):
            os.mkdir(out_dir)
        if not osp.exists(out_img):
            os.mkdir(out_img)
        if not osp.exists(out_label):
            os.mkdir(out_label)

        data = json.load(open(json_file))
        imageData = data.get("imageData")

        if not imageData:
            imagePath = json_file.split(".")[0] + img_type
            with open(imagePath, "rb") as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode("utf-8")
        # img = utils.img_b64_to_arr(imageData)
        img = json_file.split(".")[0] + ".png"
        print(img)
        img =cv2.imread(img)
        lbl, _ = utils.shapes_to_label(
            img.shape, data["shapes"], label_name_to_value
        )

        label_names = [None] * (max(label_name_to_value.values()) + 1)
        for name, value in label_name_to_value.items():
            label_names[value] = name

        lbl_viz = label2rgb(
            label=lbl, img=asgray(img), label_names=label_names, loc="rb"
        )

        PIL.Image.fromarray(img).save(osp.join(out_img, "{}.png".format(img_name)))
        utils.lblsave(osp.join(out_label, "{}.png".format(img_name)), lbl)
        PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, "{}.png".format(img_name)))

        with open(osp.join(out_dir, "label_names.txt"), "w") as f:
            for lbl_name in label_names:
                f.write(lbl_name + "\n")

    print("All Done!!!")


if __name__ == "__main__":
    json_file_path = "/media/dp/LinuxData/DataSets/temp/1218"
    out_dir = "/media/dp/LinuxData/DataSets/temp/out"
    # 需要将标签名对应的编码写到这里
    label_name_to_value = {"_background_": 0, "defect": 1}
    main(json_file_path, out_dir, label_name_to_value)
