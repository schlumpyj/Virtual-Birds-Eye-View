import cv2 as cv
import numpy as np
vid2 = cv.VideoCapture(1)
vid3 = cv.VideoCapture(2)
preImg1 = np.zeros((400, 300), np.uint8)
preImg2 = np.zeros((400, 300), np.uint8)
preImg3 = np.zeros((400, 300), np.uint8)

img2 = np.zeros((640, 480), np.uint8)
img3 = np.zeros((640, 480), np.uint8)

src = np.array([[0,150],[400,150],[400,300],[0,300]],np.float32)
dst = np.array([[0,0],[400,0],[250,150],[150,150]],np.float32)


class MyFilter:
    
    
    def process(self, img1):
        '''
            :param img: A numpy array representing the input image
            :returns: A numpy array to send to the mjpg-streamer output plugin
        '''
        vid2.read(img2)
        vid3.read(img3)
        cv.resize(img1, (400,300), dst=preImg1)
        cv.resize(img2, (400,300), dst=preImg2)
        cv.resize(img3, (400,300), dst=preImg3)
        image = np.zeros((400, 400), np.uint8)
        image2 = np.zeros((400, 400), np.uint8)

        M = cv.getPerspectiveTransform(src, dst)
        warp = cv.warpPerspective(preImg1.view(), M, (400, 300))



        two = cv.warpPerspective(preImg2.view(), M, (400, 300))
        two = cv.resize(two,(0,0), fx=2, fy=2)

        three = cv.warpPerspective(preImg3.view(), M, (400, 300))
        three = cv.resize(three,(0,0), fx=2, fy=2)
        
        image2[:warp.shape[0], :warp.shape[1]]= warp
        twoR = cv.getRotationMatrix2D((400,300),90,.5)
        twoD = cv.warpAffine(two,twoR,(two.shape[1],two.shape[0]))

        threeR = cv.getRotationMatrix2D((400,300),180,.5)
        threeD = cv.warpAffine(three,threeR,(three.shape[1],three.shape[0]))

        twoD = twoD[100:500, 250:500]
        threeD = threeD[200:450, 200:600]
        image[0:twoD.shape[0]+0, 0:twoD.shape[1]+0]= twoD
        image2[150:threeD.shape[0]+250, 0:threeD.shape[1]]=threeD
        ora = cv.add(image, image2)
        
        return preImg1
        
def init_filter():
    '''
        This function is called after the filter module is imported. It MUST
        return a callable object (such as a function or bound method). 
    '''
    f = MyFilter()
    return f.process

