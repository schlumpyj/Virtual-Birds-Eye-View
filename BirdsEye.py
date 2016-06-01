import cv2 as cv
import numpy as np

img1 = cv.imread("testBird.jpg", cv.IMREAD_COLOR)
src = np.array([[0,0],[480,0],[480,360],[0,360]],np.float32)#The orginal image points
dst = np.array([[0,120],[480,360],[450,120],[0,360]],np.float32)#I don't know exactly what the destination points would be...

M = cv.getPerspectiveTransform(src, dst)
warp = cv.warpPerspective(img1.copy(), M, (480, 360))
cv.imshow('image', img1)
cv.imshow('transform', warp)
cv.waitKey(0)
cv.destroyAllWindows()


