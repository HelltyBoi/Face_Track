from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy
import stepper


RES_CONST = 1

face_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml")

camera = PiCamera()
camera.resolution = (640*RES_CONST, 480*RES_CONST)
camera.framerate = 50
rawCapture = PiRGBArray(camera, size=(640*RES_CONST, 480*RES_CONST))

time.sleep(0.1)

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
    frame = image.array
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(frame, scaleFactor=1.25, minNeighbors = 5)
    
    if len(faces)>0:
        
        x_position = frame.shape[1]/2 - (faces[0][0] + faces[0][2]/2)
        y_position = frame.shape[0]/2 - (faces[0][1] + faces[0][3]/2)
        
        #print(x_position)
        #print(y_position)
        
        x_center = int(faces[0][0] + faces[0][2]/2)
        y_center = int(faces[0][1] + faces[0][3]/2)
        
        if y_position > 20 or x_position > 20 or x_position < -20 or y_position < -20 :
            
            for x,y,w,h in faces :
                frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
                
            x = x_center - (faces[0][2]/2)*(x_position*2/frame.shape[1])*1.5
            y = y_center + (faces[0][3]/2)*(y_position*2/frame.shape[0])*1.5
            
            frame = cv2.circle(frame, (int(x),int(y)), 2, (0,255,0), 2)
            
            if y_position <= 20 and y_position >= -20:
                frame = cv2.line(frame, (0,y_center),(frame.shape[1], y_center), (0,255,0), 1)
            else:
                frame = cv2.line(frame, (0,y_center),(frame.shape[1], y_center), (0,0,255), 1)
            
            if x_position <= 20 and x_position >= -20:
                frame = cv2.line(frame, (x_center,0),(x_center, frame.shape[1]), (0,255,0), 1)
            else:
                frame = cv2.line(frame, (x_center,0),(x_center, frame.shape[1]), (0,0,255), 1)
                
            for i in range(4):
                if y_position > 5 :
                    stepper.up(1000)
                if x_position > 5 :
                    stepper.left(1000)
                if x_position < -5 :
                    stepper.right(1000)
                if y_position < -5 :
                    stepper.down(1000)
        else:
    
            for x,y,w,h in faces:
                frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    
    if key == ord("q"):
        break

cv2.destroyAllWindows()