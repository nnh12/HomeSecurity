import RPi.GPIO as GPIO
import time
from gpiozero import Button, MotionSensor
from picamera import PiCamera
from time import sleep
from signal import pause

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

camera = PiCamera()
#class motionSensor():

    #def Detect(self):

number = 0

while True:
            
    a = 0;
    i=GPIO.input(11)
            
    if i==0:                 #When output from motion sensor is LOW
        print("No intruders")
        print(a)
        a = a + 1
            
    time.sleep(0.1)
    ##camera.capture('/home/pi/home-security/pictures/image.jpg')
    
    if i==1:   
        number = number + 1 
        ##camera.capture('/home/pi/home-security/pictures/image_%s.jpg' % number)
        ##camera.capture('/home/pi/home-security/pictures/image.jpg')
        print("Intruder detected")
        time.sleep(0.1)


