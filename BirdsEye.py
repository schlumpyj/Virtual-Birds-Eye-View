import cv2 as cv
import numpy as np
vid2 = cv.VideoCapture(1)
vid3 = cv.VideoCapture(2)

preImg1 = np.zeros((300, 400, 3), np.uint8)
preImg2 = np.zeros((300, 400, 3), np.uint8)
preImg3 = np.zeros((300, 400, 3), np.uint8)

img2 = np.zeros((480, 640, 3), np.uint8)
img3 = np.zeros((480, 640, 3), np.uint8)

image = np.zeros((400, 400, 3), np.uint8)
image2 = np.zeros((400, 400, 3), np.uint8)

finalSave = np.zeros((400, 400, 3), np.uint8)

resizeMe = np.zeros((600, 800, 3), np.uint8)
resizeMe2 = np.zeros((600, 800, 3), np.uint8)

warpMe = np.zeros((300, 400, 3), np.uint8)
warpMe2 = np.zeros((300, 400, 3), np.uint8)
warpMe3 = np.zeros((300, 400, 3), np.uint8)

rotation = np.zeros((300, 400, 3), np.uint8)
rotation2 = np.zeros((300, 400, 3), np.uint8)

src = np.array([[0,150],[400,150],[400,300],[0,300]],np.float32)
dst = np.array([[0,0],[400,0],[250,150],[150,150]],np.float32)

twoR = cv.getRotationMatrix2D((400,300),90,.5)
threeR = cv.getRotationMatrix2D((400,300),180,.5)

class MyFilter:
    
    
    def process(self, img1):

        vid2.read(img2)
        vid3.read(img3)
        cv.resize(img1, (400,300), dst=preImg1)
        cv.resize(img2, (400,300), dst=preImg2)
        cv.resize(img3, (400,300), dst=preImg3)
        #img1 = cv.flip(img1, 0)
        #img1 = cv.flip(img1, 1)
        #img2 = cv.flip(img2, 0)
        #img2 = cv.flip(img2, 1)
        #img3 = cv.flip(img3, 0)
        #img3 = cv.flip(img3, 1)

        M = cv.getPerspectiveTransform(src, dst)
        
        cv.warpPerspective(preImg1, M, (400, 300), dst=warpMe)

        cv.warpPerspective(preImg2, M,(400, 300), dst=warpMe2)
        cv.resize(warpMe2,(0,0), dst=resizeMe, fx=2, fy=2)

        cv.warpPerspective(preImg3, M,(400, 300), dst=warpMe3)
        cv.resize(warpMe3,(0,0), dst=resizeMe2, fx=2, fy=2)
        
        image2[:warpMe.shape[0], :warpMe.shape[1]]= warpMe
        
        rotation = cv.warpAffine(resizeMe,twoR,(resizeMe.shape[1],resizeMe.shape[0]))
        rotation2 = cv.warpAffine(resizeMe2,threeR,(resizeMe2.shape[1],resizeMe2.shape[0]))#could rid of this .shape stuff

        rotation = rotation[100:500, 250:500]
        rotation2 = rotation2[200:450, 200:600]
        image[0:rotation.shape[0]+0, 0:rotation.shape[1]+0]= rotation
        image2[150:rotation2.shape[0]+250, 0:rotation2.shape[1]]=rotation2
        ora = cv.add(image, image2, dst=finalSave)
        return ora
        
def init_filter():
    '''
        This function is called after the filter module is imported. It MUST
        return a callable object (such as a function or bound method). 
    '''
    f = MyFilter()
    return f.process

