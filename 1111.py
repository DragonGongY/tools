import os
import glob
import shutil


for img in glob.glob("/media/dp/LinuxData/DataSets/GuanGan/RJQ/images/*.xml"):
    print(img)
    shutil.move(img, "/media/dp/LinuxData/DataSets/GuanGan/RJQ/")
    name = img.split(".")[0] + ".jpg"
    shutil.move(name, "/media/dp/LinuxData/DataSets/GuanGan/RJQ/")