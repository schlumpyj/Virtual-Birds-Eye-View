from threading import Thread
import time
import numpy as np
import cv2
 
class WebcamVideoStream:
    
    def __init__(self, camera, src=0):

        self.stream = cv2.VideoCapture(src)
        self.face = cv2.CascadeClassifier('/home/josh/Downloads/face.xml')
        self.faces=None
        if camera==1:
            self.frame = np.zeros((240, 320, 3), np.uint8)
        else:
            self.frame = np.zeros((480, 640, 3), np.uint8)
        self.stream.read(self.frame)
        self.stopped = False
        
    def start(self):

        Thread(target=self.update, args=()).start()
        Thread(target=self.haarMe, args=()).start()
        return self
 
    def update(self):
	
        while True:	
            if self.stopped:
                self.stream.release()
                return   
            self.stream.read(self.frame)

    def haarMe(self):
        while True:
            if self.stopped:
                return
            frame  = cv2.resize(self.frame, (320, 240))
            gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.faces=self.face.detectMultiScale(gray, 1.2, 2)

    def readHaar(self):
        return self.faces

    def read(self):
            
        return self.frame

    def stop(self):

        self.stopped = True
