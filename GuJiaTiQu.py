import cv2
import numpy as np
from skimage import morphology
import time

print(cv2.__version__)
img = cv2.imread(r"G:\8.png", 0)
erode = cv2.erode(img, (17, 17), iterations=3)
dilate = cv2.dilate(erode, (15,15), iterations=6)

ret, th1 = cv2.threshold(dilate, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

#实施骨架算法
th1[th1==255] = 1
start = time.time()
skeleton =morphology.skeletonize(th1, method='zhang')
skeleton = skeleton.astype(np.uint8)*255
skeleton = 255-skeleton
print(time.time() - start)


cv2.imshow("erode", erode)
cv2.imshow("dilate", dilate)
cv2.imshow("th1", th1)
cv2.imshow("skeleton", skeleton)

cv2.waitKey()