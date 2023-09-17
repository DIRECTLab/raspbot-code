from picamera2 import Picamera2
import time
import cv2

if __name__ == '__main__':
    picam2 = Picamera2()
    picam2.start()
    
    array = picam2.capture_array()

    cv2.imshow('Image', array)
    cv2.waitKey(0)

    
