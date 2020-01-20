import time
import RPi.GPIO as GPIO

pinsx = [25,8,7,1]
pinsy = [6,13,19,26]

stepper_seq = [[1,0,0,0],
               [1,1,0,0],
               [0,1,0,0],
               [0,1,1,0],
               [0,0,1,0],
               [0,0,1,1],
               [0,0,0,1],
               [1,0,0,1]]

GPIO.setmode(GPIO.BCM)
    
def left(speed):
    
    for i in range(4):
        GPIO.setup(pinsx[i],GPIO.OUT)
        GPIO.setup(pinsy[i],GPIO.OUT)
        
    for i in range(8):
        for j in range(4):
            GPIO.output(pinsx[j],stepper_seq[7-i][j])
        time.sleep(1/speed)
        
    for i in range(4):
        GPIO.cleanup(pinsx[i])
        GPIO.cleanup(pinsy[i])
        
def right(speed):
    
    for i in range(4):
        GPIO.setup(pinsx[i],GPIO.OUT)
        GPIO.setup(pinsy[i],GPIO.OUT)
    
    for i in range(8):
        for j in range(4):
            GPIO.output(pinsx[j],stepper_seq[i][j])
        time.sleep(1/speed)
        
    for i in range(4):
        GPIO.cleanup(pinsx[i])
        GPIO.cleanup(pinsy[i])
        
def down(speed):
    
    for i in range(4):
        GPIO.setup(pinsx[i],GPIO.OUT)
        GPIO.setup(pinsy[i],GPIO.OUT)
    
    for i in range(8):
        for j in range(4):
            GPIO.output(pinsy[j], stepper_seq[7-i][j])
        time.sleep(1/speed)
        
    for i in range(4):
        GPIO.cleanup(pinsx[i])
        GPIO.cleanup(pinsy[i])

def up(speed):
    
    for i in range(4):
        GPIO.setup(pinsx[i],GPIO.OUT)
        GPIO.setup(pinsy[i],GPIO.OUT)
    
    for i in range(8):
        for j in range(4):
            GPIO.output(pinsy[j],stepper_seq[i][j])
        time.sleep(1/speed)
        
    for i in range(4):
        GPIO.cleanup(pinsx[i])
        GPIO.cleanup(pinsy[i])
      
up(20)
left(20)
    
down(20)
left(20)
            
