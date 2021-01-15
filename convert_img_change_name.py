import cv2
import os
import shutil

imgs_save_path="/home/dp/dataset/Tower_dataset/Covered/images"
annotations_save_path = '/home/dp/dataset/Tower_dataset/Covered/annotations'

root = "/home/dp/dataset/Tower_dataset"
for folder in os.listdir(root):
    filePath = os.path.join(root, folder)
    for imgs in os.listdir(filePath):
        if imgs.endswith("txt"):
            continue
        if imgs == "JPEGImages":
            pass
            # imgspath = os.path.join(filePath, imgs)
            # for img in os.listdir(imgspath):
            #     imgpath = os.path.join(imgspath, img)
            #     img_read = cv2.imread(imgpath)
            #     imgName = img.split(".")[0]
            #     if os.path.exists(imgs_save_path + '/' + imgName + ".png"):
            #         pass
            #     else:
            #         cv2.imwrite(imgs_save_path + '/' + imgName + ".png", img_read)
            #     print(imgpath)
        if imgs == "SegmentationClassPNG":
            labelspath = os.path.join(filePath, imgs)
            for label in os.listdir(labelspath):
                labelName = label.split(".")[0]
                label = os.path.join(labelspath, label)
                shutil.copy(label, annotations_save_path)
                print(label)
