
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.rotation = 180
camera.capture('/home/pi/home-security/picture.jpg')
camera.stop_preview()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

# camera = picamera


# #image image names


while (True):
    i = GPIO.input(11) 
    if (i ==1):
        print("hi")
        camera.capture('/home/pi/home-security/picture.jpg')
   

