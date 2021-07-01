#coding: utf-8
import Augmentor
import glob
import os

import cv2
import numpy as np

class ImgAug_Lbl():
    """
    对分割数据集的图片和标签同时进行数据增强处理
    """
    def aug(self, img_dir, label_dir, aug_num):
        p = Augmentor.Pipeline(img_dir)
        p.ground_truth(label_dir)

        p.skew_corner(probability=0.5, magnitude=0.2)
        p.skew_tilt(probability=0.5, magnitude=0.2)
        p.skew_left_right(probability=0.5,magnitude=0.2)
        p.shear(probability=0.5, max_shear_left=0.7, max_shear_right=0.7)
        # p.random_distortion(probability=1, grid_height=1, grid_width=1, magnitude=1)
        # p.zoom(probability=1, min_factor=0.7, max_factor=1.3)

        # p.flip_random(probability=0.5)
        p.rotate(probability=0.5, max_left_rotation=1, max_right_rotation=1)
        p.flip_left_right(probability=0.5)
        # p.flip_top_bottom(probability=0.5)

        p.sample(aug_num, multi_threaded=True)

    def is_exits(self, aug_outimg_dir, aug_outanno_dir):
        """
        判断图片路径和标签路径是否存在，不存在进行路径创建
        aug_outimg_dir：增强图片保存路径
        aug_outanno_dir: 增强标签保存路径
        """
        if not os.path.exists(aug_outimg_dir) or not os.path.exists(aug_outanno_dir):
            self.aug_outimg_dir = aug_outimg_dir
            self.aug_outanno_dir = aug_outanno_dir
            os.mkdir(self.aug_outimg_dir)
            os.mkdir(self.aug_outanno_dir)
            print("check path whether exist!!!!!!!!!!!!!!!!1")

    def seprate_imgs(self, augmentor_output):
        """
        将Augmentor增强的图片进行分开
        augmentor_output：Augmentor工具增强后输出的图片路径
        """
        all_imgs = os.listdir(augmentor_output)
        for name in all_imgs:
            # 增强后标签文件名中会有"groundtruth"字段
            if "groundtruth" in name:
                gt_new_name = name.split("_")[-1]
                gt_out = os.path.join(self.aug_outanno_dir, gt_new_name)
                orignal_path = os.path.join(augmentor_output, name)
                os.renames(orignal_path, gt_out)
            # 增强后图片文件名中会有"original"字段
            if "original" in name:
                img_new_name = name.split("_")[-1]
                img_out = os.path.join(self.aug_outimg_dir, img_new_name)
                orignal_path = os.path.join(augmentor_output, name)
                os.renames(orignal_path, img_out)
        print("image seprate !!!!!!!!!!!!!!!!!!!!!!!!")

    def delete_(self):
        """
        删除生成中多余出来的图片
        """
        annos = os.listdir(self.aug_outanno_dir)
        for img_name in os.listdir(self.aug_outimg_dir):
            if img_name in annos:
                pass
            else:
                os.remove(os.path.join(self.aug_outimg_dir, img_name))
        print("delete images cant pair !!!!!!!!!!!!")

    def check_pair(self):
        """
        检查图片和标签是否成对出现
        """
        imgs = sorted(os.listdir(self.aug_outimg_dir))
        annos = sorted(os.listdir(self.aug_outanno_dir))
        imgtotals = len(imgs)
        annototals = len(annos)
        for i in range(imgtotals):
            if (imgtotals == annototals) and (imgs[i] == annos[i]):
                print("pair")
            else:
                print("error", imgtotals[i])

        print("check pair !!!!!!!!!!!!!!!!!")


class ImgAug_NoneSize():
    """
    对图像的亮度、对比度、颜色进行增强处理，并生成相应标签
    """
    def __init__(self, img_dir, aug_num):
        self.img_dir = img_dir
        p = Augmentor.Pipeline(self.img_dir)
        p.random_contrast(probability=1, min_factor=0.5, max_factor=1.5)
        p.random_brightness(probability=1, min_factor=0.5, max_factor=1.5)
        p.random_color(probability=1, min_factor=0.5, max_factor=1.5)
        p.sample(aug_num, multi_threaded=True)
        print("segment None size !!!!!!!!!!!!!!!!!")

    def generate_lbl(self, img_dir, lbl_dir, output_img_dir, output_gt_dir):
        """
        lbl_dir: 原始标签路径
        aug_img_dir: 增强后图片的路径
        output_img_dir: 输出图片路径
        output_gt_dir: 输出标签路径
        """
        gt_names = os.listdir(lbl_dir)
        aug_names = os.listdir(img_dir)
        if not os.path.exists(output_img_dir) or not os.path.exists(output_gt_dir):
            os.mkdir(output_img_dir)
            os.mkdir(output_gt_dir)
        for augname in aug_names:
            for gtname in gt_names:
                # 增强后的图片中包含 "img_original_"+图片名+"_" 字段
                if "_original_"+gtname+"_" in augname:

                    gt_img = cv2.imread(os.path.join(lbl_dir, gtname))
                    gt_newname = augname

                    img_path = os.path.join(img_dir, augname)
                    img_ = cv2.imread(img_path)
                    imgOutPath = os.path.join(output_img_dir, augname)
                    cv2.imwrite(imgOutPath, img_)

                    gtOutPath = os.path.join(output_gt_dir, gt_newname)
                    cv2.imwrite(gtOutPath, gt_img)

        print("generate label !!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    imgPath = "/media/dp/LinuxData/DataSets/huihua/data_face/third/imgs"
    labelPath = "/media/dp/LinuxData/DataSets/huihua/data_face/third/gt"

    # #######################
    imgout_dir = "/media/dp/LinuxData/DataSets/huihua/data_face/third/img_aug"
    labelout_dir = "/media/dp/LinuxData/DataSets/huihua/data_face/third/lbl_aug"

    # aug = ImgAug_Lbl()
    # # aug.aug(imgPath, labelPath, 1000)
    # aug.is_exits(imgout_dir, labelout_dir)
    # aug.seprate_imgs(os.path.join(imgPath, "output"))
    # aug.delete_()
    # aug.check_pair()

    # #########################
    imgs_dir = "/media/dp/LinuxData/DataSets/huihua/data_face/third/totals/imgs"
    label_dir = "/media/dp/LinuxData/DataSets/huihua/data_face/third/totals/gts"
    NoneSizeAug = ImgAug_NoneSize(imgs_dir, 3000)
    NoneSizeAug.generate_lbl(os.path.join(imgs_dir, "output"),
                             label_dir,
                             "/media/dp/LinuxData/DataSets/huihua/data_face/third/augimg",
                             "/media/dp/LinuxData/DataSets/huihua/data_face/third/auggt")
