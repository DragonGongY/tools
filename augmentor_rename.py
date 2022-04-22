import os

root = "/home/dp/Documents/datasets/DPQ/coverd/train/output"
imgs = os.path.join(root, "imgs")
labels = os.path.join(root, "labels")
rename_imgs = os.path.join(root, "ims")
rename_gts = os.path.join(root, "gts")

for im in os.listdir(imgs):
    imgpath = os.path.join(imgs, im)
    filename = im.split("train_original_")[-1]
    os.renames(imgpath, os.path.join(rename_imgs, filename))

    gt_name = "_groundtruth_(1)_train_" + filename
    os.renames(os.path.join(labels, gt_name), os.path.join(rename_gts, filename))

# img = "/home/dp/Documents/datasets/DPQ/coverd/train/output/train_original_00001_3.png_a78bf119-aaed-4516-95b2-e18f7b590435.png"
# im = img.split("train_original_")[-1]
#
# gt = "/home/dp/Documents/datasets/DPQ/coverd/train/output/_groundtruth_(1)_train_00001_3.png_a78bf119-aaed-4516-95b2-e18f7b590435.png"
# g = gt.split("_groundtruth_(1)_train_")[-1]
#
# print(im == g)