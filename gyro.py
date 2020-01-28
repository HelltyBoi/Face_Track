import smbus
import time
import math

bus = smbus.SMBus(1)
filtar = 65534
def xAngle():
    bus.write_byte_data(0x68,0x6B,0x00)
    bus.write_byte_data(0x68,0x1B,0x18)
    read=bus.read_byte_data(0x68,0x1A)
    
    read=bus.read_byte_data(0x68,0x3D)
    accY=read<<8
    read=bus.read_byte_data(0x68,0x3E)
    accY=accY+read
    if(accY>>15==1):
        accY=accY^filtar
        accY=-(accY+1)

        
    read=bus.read_byte_data(0x68,0x3F)
    accZ=read<<8
    read=bus.read_byte_data(0x68,0x40)
    accZ=accZ+read
    if(accZ>>15==1):
        accZ=accZ^filtar
        accZ=-(accZ+1)
    
    return (math.atan2(accY,accZ))*(180/math.pi)
    
def yAngle():
    bus.write_byte_data(0x68,0x6B,0x00)
    bus.write_byte_data(0x68,0x1B,0x18)
    read=bus.read_byte_data(0x68,0x1A)
    
    read=bus.read_byte_data(0x68,0x3B)
    accX=read<<8
    read=bus.read_byte_data(0x68,0x3C)
    accX=accX+read
    if(accX>>15==1):
        accX=accX^filtar
        accX=-(accX+1)
        
    read=bus.read_byte_data(0x68,0x3F)
    accZ=read<<8
    read=bus.read_byte_data(0x68,0x40)
    accZ=accZ+read
    if(accZ>>15==1):
        accZ=accZ^filtar
        accZ=-(accZ+1)
 
    return (math.atan2(accX,accZ))*(180/math.pi)

def zAngle():
    bus.write_byte_data(0x68,0x6B,0x00)
    bus.write_byte_data(0x68,0x1B,0x18)
    read=bus.read_byte_data(0x68,0x1A)
    
    read=bus.read_byte_data(0x68,0x3B)
    accX=read<<8
    read=bus.read_byte_data(0x68,0x3C)
    accX=accX+read
    if(accX>>15==1):
        accX=accX^filtar
        accX=-(accX+1)
        
    read=bus.read_byte_data(0x68,0x3D)
    accY=read<<8
    read=bus.read_byte_data(0x68,0x3E)
    accY=accY+read
    if(accY>>15==1):
        accY=accY^filtar
        accY=-(accY+1)
        
    return (math.atan2(accX,accY))*(180/math.pi)

    
print(xAngle())
print(yAngle())
print(zAngle())