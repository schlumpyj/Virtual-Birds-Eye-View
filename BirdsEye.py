import cv2 as cv
import numpy as np
from webcamGet import WebcamVideoStream
vid2 = WebcamVideoStream(src=1).start()
vid3 = WebcamVideoStream(src=2).start()
vid4 = WebcamVideoStream(src="http://roborio-4480-frc.lan:5800/?action=stream").start()
preImg1 = np.zeros((300, 400, 3), np.uint8)
preImg2 = np.zeros((300, 400, 3), np.uint8)
preImg3 = np.zeros((300, 400, 3), np.uint8)
preImg4 = np.zeros((300, 400, 3), np.uint8)

img2 = np.zeros((480, 640, 3), np.uint8)
img3 = np.zeros((480, 640, 3), np.uint8)
img4 = np.zeros((240, 320, 3), np.uint8)

image = np.zeros((400, 400, 3), np.uint8)
image2 = np.zeros((400, 400, 3), np.uint8)

finalSave = np.zeros((400, 400, 3), np.uint8)

resizeMe = np.zeros((600, 800, 3), np.uint8)
resizeMe2 = np.zeros((600, 800, 3), np.uint8)
resizeMe3 = np.zeros((600, 800, 3), np.uint8)

warpMe = np.zeros((300, 400, 3), np.uint8)
warpMe2 = np.zeros((300, 400, 3), np.uint8)
warpMe3 = np.zeros((300, 400, 3), np.uint8)
warpMe4 = np.zeros((300, 400, 3), np.uint8)

rotation = np.zeros((300, 400, 3), np.uint8)
rotation2 = np.zeros((300, 400, 3), np.uint8)
rotation3 = np.zeros((300, 400, 3), np.uint8)

src = np.array([[0,150],[400,150],[400,300],[0,300]],np.float32)
dst = np.array([[0,0],[400,0],[250,150],[150,150]],np.float32)
M = cv.getPerspectiveTransform(src, dst)

twoR = cv.getRotationMatrix2D((400,300),90,.5)
threeR = cv.getRotationMatrix2D((400,300),180,.5)
fourR = cv.getRotationMatrix2D((400,300),270,.5)

class MyFilter:
    
    
    def process(self, img1):
        img2 = vid2.read() #needs dst in webcamstream file
        img3 = vid3.read()
        img4 = vid4.read()
        cv.resize(img1, (400,300), dst=preImg1)
        cv.resize(img2, (400,300), dst=preImg2)
        cv.resize(img3, (400,300), dst=preImg3)
        cv.resize(img4, (400,300), dst=preImg4)

        #img1 = cv.flip(img1, 0)
        #img1 = cv.flip(img1, 1)
        #img2s = cv.flip(img2, 0) #needs dst
        #img2s = cv.flip(img2, 1)
        #img3 = cv.flip(img3, 0)
        #img3 = cv.flip(img3, 1)
        #img4 = cv.flip(img4, 0)
        #img4 = cv.flip(img4, 1)
        
        cv.warpPerspective(preImg1, M, (400, 300), dst=warpMe)

        cv.warpPerspective(preImg2, M,(400, 300), dst=warpMe2)
        cv.resize(warpMe2,(0,0), dst=resizeMe, fx=2, fy=2)

        cv.warpPerspective(preImg3, M,(400, 300), dst=warpMe3)
        cv.resize(warpMe3,(0,0), dst=resizeMe2, fx=2, fy=2)

        cv.warpPerspective(preImg4, M,(400, 300), dst=warpMe4)
        cv.resize(warpMe4,(0,0), dst=resizeMe3, fx=2, fy=2)
        
        image2[:warpMe.shape[0], :warpMe.shape[1]]= warpMe
        
        rotation = cv.warpAffine(resizeMe,twoR,(resizeMe.shape[1],resizeMe.shape[0]))
        rotation2 = cv.warpAffine(resizeMe2,threeR,(resizeMe2.shape[1],resizeMe2.shape[0]))#could rid of this
        rotation3 = cv.warpAffine(resizeMe3,fourR,(resizeMe3.shape[1],resizeMe3.shape[0]))

        rotation = rotation[100:500, 250:500]
        rotation2 = rotation2[200:450, 200:600]
        rotation3 = rotation3[100:500, 400:550]
        
        image[0:rotation.shape[0]+0, 0:rotation.shape[1]+0]= rotation
        image[0:rotation3.shape[0]+0, 250:rotation3.shape[1]+250] = rotation3
        
        image2[150:rotation2.shape[0]+250, 0:rotation2.shape[1]]=rotation2
        
        cv.add(image, image2, dst=finalSave)
        return finalSave
        
def init_filter():

    f = MyFilter()
    return f.process

