import Augmentor
import glob
import os
import numpy as np

def AugSeg(img_file, label_file):
    p = Augmentor.Pipeline(img_file)
    p.ground_truth(label_file)

    p.skew_corner(probability=1, magnitude=0.7)
    p.skew_tilt(probability=1, magnitude=0.5)
    p.shear(probability=1, max_shear_left=5, max_shear_right=5)
    p.random_distortion(probability=1, grid_height=4, grid_width=4, magnitude=2)
    p.rotate(probability=1, max_left_rotation=2, max_right_rotation=2)
    p.flip_left_right(probability=0.5)
    p.flip_top_bottom(probability=0.5)

    p.sample(3000, multi_threaded=True)


if __name__ == "__main__":
    imgPath = "/home/dp/Documents/datasets/DPQ/coverd/train"
    labelPath = "/home/dp/Documents/datasets/DPQ/coverd/train_labels"
    AugSeg(imgPath, labelPath)