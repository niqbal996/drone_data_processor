import cv2#
import numpy as np
from tifffile import TiffFile

file = TiffFile('/home/niqbal/ruebe_17408_23552.tiff')

img_array = file.asarray()

cv_image = img_array[:, :, 0:3]  # BGR
blue = cv_image[:, :, 0]
green = cv_image[:, :, 1]
red = cv_image[:, :, 2]

cv_image = cv_image / 65535   # (2**16 - 1)
cv_image = cv_image * 255     # (2**8 - 1)
cv_image = cv_image.astype(np.uint8)
print('hold')
# cv2.imshow('image', cv_image)
# cv2.waitKey()
cv2.imwrite('/home/niqbal/ruebe_17408_23552.png', cv_image)