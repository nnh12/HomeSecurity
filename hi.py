import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import RPi.GPIO as GPIO
import time
from gpiozero import Button, MotionSensor
from picamera import PiCamera
from time import sleep
from signal import pause
import sched, time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin


s = sched.scheduler(time.time, time.sleep)
a = "new"

PAGE="""\
<html>
<head>
  <title>HTML Elements Reference</title>
</head>
<body>
<h1>This is a heading</h1>
<img src="image.jpg" alt="Flowers in Chania">
<p>This is a paragraph.</p>

</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            print('hello')
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    i = GPIO.input(11)
                    a = 0
                    if ( i == 1):
                      if ( a == 0):
                        camera.capture('/home/pi/home-security/pictures/nathanHsiao.jpg')
                      variable = 25
                      print("intruder")

                    a = 1
                    
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    print("stream server")

def println():
    print('hello')

def motion_detected():     
    a = 0;
    i= GPIO.input(11)
            
    if i==0:                
        print("No intruders")
        print(a)
        a = a + 1
            
    time.sleep(0.1)
    
    if i==1:   
        number = number + 1 
        print("Intruder detected")
        time.sleep(0.1)

def print_time(a='default'):
    print("From print_time", time.time(), a)

def print_some_times():
    print(time.time())
    s.enter(1, 1, print_time)
    s.enter(1, 2, print_time, argument=('positional',))
    s.enter(1, 1, print_time, kwargs={'a': 'keyword'})
    s.run()
    print(time.time())

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    print_some_times()

    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
        print("hello")

    finally:
        camera.stop_recording()