import cv2 as cv
import numpy as np

img1 = cv.imread("testBird.jpg", cv.IMREAD_COLOR)
src = np.array([[0,0],[480,0],[480,360],[0,360]],np.float32)
dst = np.array([[0,120],[480,360],[450,120],[0,360]],np.float32)

M = cv.getPerspectiveTransform(src, dst)
warp = cv.warpPerspective(img1.copy(), M, (450, 300))
cv.imshow('image', img1)
cv.imshow('transform', warp)
cv.waitKey(0)
cv.destroyAllWindows()


