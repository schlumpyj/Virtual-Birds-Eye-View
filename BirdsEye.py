import cv2 as cv
import numpy as np
import time

vid1 = cv.VideoCapture(0)
vid2 = cv.VideoCapture("http://10.44.80.61:5800/?action=stream")
vid1.set(6, cv.VideoWriter_fourcc(*"MJPG"))#Should set the codec, but it doesn't
vid1.set(10, 50)
vid1.set(3, 640)
vid1.set(4, 480)
vid2.set(6, cv.VideoWriter_fourcc(*"MJPG"))#Should set the codec, but it doesn't
vid2.set(10, 50)
vid2.set(3, 640)
vid2.set(4, 480)

fourcc = cv.VideoWriter_fourcc(*'DIV3')
out1 = cv.VideoWriter('try.avi',fourcc, 20.0, (640,480))
out2 = cv.VideoWriter('try2.avi',fourcc, 20.0, (640,480))
start = time.time()
counter =0
while True:
    _, img1 = vid1.read()
    _, img2 = vid2.read()
    out1.write(img1)
    out2.write(img2)
    counter+=1
    img1 = cv.resize(img1, (480, 360))
    img2 = cv.resize(img2, (480, 360))
    image = np.zeros((500, 500, 3), np.uint8)
    image2 = np.zeros((500, 500, 3), np.uint8) 
    src = np.array([[0,200],[480,200],[480,360],[0,360]],np.float32)
    dst = np.array([[0,0],[480,0],[300,200],[180,200]],np.float32)
    ##########################Pushing   ^^ Down to below 200 gives the weird image

    M = cv.getPerspectiveTransform(src, dst)
    warp = cv.warpPerspective(img1.copy(), M, (480, 360))



    two = cv.warpPerspective(img2.copy(), M, (480, 360))
    two = cv.resize(two,(0,0), fx=2, fy=2)


    image2[:warp.shape[0], 15:warp.shape[1]+15]= warp
    twoR = cv.getRotationMatrix2D((two.shape[1]/2,two.shape[0]/2),90,.5)
    twoD = cv.warpAffine(two,twoR,(two.shape[1],two.shape[0]))

    twoD = twoD[100:600, 310:500]

    image[0:twoD.shape[0]+0, 0:twoD.shape[1]+0]= twoD

    ora = cv.add(image, image2)
    cv.imshow("image", ora)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
print counter/(time.time()-start)
vid1.release()
vid2.release()
cv.destroyAllWindows()
