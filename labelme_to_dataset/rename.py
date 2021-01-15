root = "/media/dp/LinuxData/DataSets/NiZiTuFu/VOC2007_putty"

import os
import shutil

for i, xml in enumerate(os.listdir(os.path.join(root, "Annotations"))):
    newxml_name = os.path.join(root, "Annotations", "{}.xml".format(i))
    newimg_name = os.path.join(root, "JPEGImages", "{}.jpg".format(i))
    imgPath = os.path.join(root, "JPEGImages", xml.split(".")[0]+".jpg")
    xmlPath = os.path.join(root, "Annotations", xml)
    os.renames(xmlPath, newxml_name)
    os.renames(imgPath, newimg_name)
