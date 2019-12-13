import numpy as np
import cv2

a, b = r, r
n = 2*r

y,x = np.ogrid[-a:n-a, -b:n-b]
mask = x*x + y*y <= r*r
array[mask] = 1.

cv2.imshow('f', array)
cv2.waitKey(0)
