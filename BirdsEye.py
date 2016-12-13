import cv2 as cv
import numpy as np
vid2 = cv.VideoCapture(1)
vid3 = cv.VideoCapture(2)
class MyFilter:
    
    
    def process(self, img1):
        '''
            :param img: A numpy array representing the input image
            :returns: A numpy array to send to the mjpg-streamer output plugin
        '''
        _, img2 = vid2.read()
        _, img3 = vid3.read()
        img1 = cv.resize(img1, (400, 300))
        img2 = cv.resize(img2, (400, 300))
        img3 = cv.resize(img3, (400, 300))
        #img1 = cv.flip(img1, 0)
        #img1 = cv.flip(img1, 1)
        #img2 = cv.flip(img2, 0)
        #img2 = cv.flip(img2, 1)
        #img3 = cv.flip(img3, 0)
        #img3 = cv.flip(img3, 1)
        image = np.zeros((400, 400, 3), np.uint8)
        image2 = np.zeros((400, 400, 3), np.uint8) 
        src = np.array([[0,150],[400,150],[400,300],[0,300]],np.float32)
        dst = np.array([[0,0],[400,0],[250,150],[150,150]],np.float32)
        ##########################Pushing   ^^ Down to below 200 gives the weird image

        M = cv.getPerspectiveTransform(src, dst)
        warp = cv.warpPerspective(img1.copy(), M, (400, 300))



        two = cv.warpPerspective(img2.copy(), M, (400, 300))
        two = cv.resize(two,(0,0), fx=2, fy=2)

        three = cv.warpPerspective(img3.copy(), M, (400, 300))
        three = cv.resize(three,(0,0), fx=2, fy=2)
        
        image2[:warp.shape[0], :warp.shape[1]]= warp
        twoR = cv.getRotationMatrix2D((two.shape[1]/2,two.shape[0]/2),90,.5)
        twoD = cv.warpAffine(two,twoR,(two.shape[1],two.shape[0]))

        threeR = cv.getRotationMatrix2D((three.shape[1]/2,three.shape[0]/2),180,.5)
        threeD = cv.warpAffine(three,threeR,(three.shape[1],three.shape[0]))

        twoD = twoD[100:500, 250:500]
        threeD = threeD[200:450, 200:600]
        image[0:twoD.shape[0]+0, 0:twoD.shape[1]+0]= twoD
        image2[150:threeD.shape[0]+250, 0:threeD.shape[1]]=threeD
        ora = cv.add(image, image2)
        return ora
        
def init_filter():
    '''
        This function is called after the filter module is imported. It MUST
        return a callable object (such as a function or bound method). 
    '''
    f = MyFilter()
    return f.process

