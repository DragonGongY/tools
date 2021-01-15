from PIL import Image
import numpy as np

img = "/home/dp/Documents/datasets/DPQ/datasets/covered/labels/00003.png"
img = Image.fromarray(np.uint8(img))

img.show()