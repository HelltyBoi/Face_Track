from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import time
import numpy
import stepper



RES_CONST = 1
STEPPER_SPEED=500

item_dict={'x_position':0.0, 'y_position':0.0}

face_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml")

camera = PiCamera()
camera.resolution = (640*RES_CONST, 480*RES_CONST)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(640*RES_CONST, 480*RES_CONST))

time.sleep(0.1)

def face_det():
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        frame = image.array
    
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(frame, scaleFactor=1.45, minNeighbors = 5)
    
        if len(faces)>0:
        
            item_dict['x_position'] = frame.shape[1]/2 - (faces[0][0] + faces[0][2]/2)
            item_dict['y_position'] = frame.shape[0]/2 - (faces[0][1] + faces[0][3]/2)
        
            #x.put_nowait(x_position)
            #y.put_nowait(y_position)
                    
            x_center = int(faces[0][0] + faces[0][2]/2)
            y_center = int(faces[0][1] + faces[0][3]/2)
        
            if item_dict['y_position'] > 20 or
            item_dict['x_position'] > 20 or
            item_dict['x_position'] < -20 or
            item_dict['y_position'] < -20 :
            
                for x,y,w,h in faces :
                    frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
                
                x = x_center - (faces[0][2]/2)*(item_dict['x_position']*2/frame.shape[1])*1.5
                y = y_center + (faces[0][3]/2)*(item_dict['y_position']*2/frame.shape[0])*1.5
            
                frame = cv2.circle(frame, (int(x),int(y)), 2, (0,255,0), 2)
            
                if item_dict['y_position'] <= 20 and item_dict['y_position'] >= -20:
                    frame = cv2.line(frame, (0,y_center),(frame.shape[1], y_center), (0,255,0), 1)
                else:
                    frame = cv2.line(frame, (0,y_center),(frame.shape[1], y_center), (0,0,255), 1)
            
                if item_dict['x_position'] <= 20 and item_dict['x_position'] >= -20:
                    frame = cv2.line(frame, (x_center,0),(x_center, frame.shape[1]), (0,255,0), 1)
                else:
                    frame = cv2.line(frame, (x_center,0),(x_center, frame.shape[1]), (0,0,255), 1) 
            else:
    
                for x,y,w,h in faces:
                    frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
                    item_dict['x_position'] = 0.0
                    item_dict['y_position'] = 0.0
        
        else:
            
            item_dict['x_position'] = 0.0
            item_dict['y_position'] = 0.0
        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
    
        if key == ord("q"):
            item_dict['x_position'] = 0.0
            item_dict['y_position'] = 0.0
            break

    cv2.destroyAllWindows()
        
def check_position():
    
    while(1):
        
        if (item_dict['y_position'] < 100 and
            item_dict['x_position'] < 100 and
            item_dict['x_position'] > -100 and
            item_dict['y_position'] > -100) :
            
            time.sleep(0.05)

        STEPPER_SPEED=900
        
        print(item_dict['x_position'])
        print(item_dict['y_position'])
        
        if item_dict['y_position'] > 20 :
            stepper.up(STEPPER_SPEED)
        if item_dict['x_position'] > 20 :
            stepper.left(STEPPER_SPEED)
        if item_dict['x_position'] < -20 :
            stepper.right(STEPPER_SPEED)
        if item_dict['y_position'] < -20 :
            stepper.down(STEPPER_SPEED)      
            
if __name__ == '__main__':

    p=Thread(target=check_position)
    o=Thread(target=face_det)
    p.start()
    o.start()
    p.join()
    o.join()