from threading import Thread
import time
import cv2
 
class WebcamVideoStream:
    
    def __init__(self, camera, src=0):

        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        if camera == 1:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.out = cv2.VideoWriter('camera1.avi', fourcc, 10.0, (320,240))
        else:
            fourcc = cv2.VideoWriter_fourcc(*'DIV3')
            self.out = cv2.VideoWriter('camera'+str(camera)+'.avi',fourcc, 10.0, (640,480))
        self.stopped = False
    def start(self):

        Thread(target=self.update, args=()).start()
        return self
 
    def update(self):
	
        while True:	
            if self.stopped:
                self.stream.release()
                return   
            (self.grabbed, self.frame) = self.stream.read()
            self.out.write(self.frame)


    def read(self):
            
        return self.frame

    def stop(self):

        self.stopped = True
