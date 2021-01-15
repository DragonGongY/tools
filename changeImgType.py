import cv2
import glob, os

img_dir = "/media/dp/LinuxData/DataSets/temp/1218"
for img in glob.glob(os.path.join(img_dir, "*.bmp")):
    _img = cv2.imread(img)
    new_type = img.split(".")[0] + ".png"
    cv2.imwrite(new_type, _img)
