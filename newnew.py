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
import RPi.GPIO as GPIO
import time
import datetime
import picamera
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin
camera = picamera.PiCamera()
s = sched.scheduler(time.time, time.sleep)

a = "new"

PAGE="""\
<html>
<head>
<style>
$off_white:#fafafa;
$light_grey:#A39D9E;
*{
  box-sizing:border-box;
}
body{
  background-color: $off_white;
}
/*.container{
  margin:100px auto;
  width:809px;
}*/
.container {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;

}
.light{
  background-color: #fff;
}
.dark{
  margin-left: 65px;
}

#power {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 27px;
  height: 30px;
  margin: -14px 0 0 -15px;
  background-image: url("/home/pi/home-security/pictures_nathanHsiao.png");
}

.calendar{
  width:600px;
  box-shadow: 0px 0px 35px -16px rgba(0,0,0,0.75);
  font-family: 'Roboto', sans-serif;
  padding: 20px 30px;
  color:#363b41;
  display: inline-block;
}
.calendar_header{
  border-bottom: 2px solid rgba(0, 0, 0, 0.08);
}
.header_copy{
  color:$light_grey;
  font-size:20px;
}
.calendar_plan{
  margin:20px 0 40px;
}
.cl_plan{/*pink box*/
  width:100%;
  height: 140px;
  background-image: linear-gradient(-222deg, #FF8494, #FFA9B7);
  box-shadow: 0px 0px 52px -18px rgba(0, 0, 0, 0.75);
  padding:30px;
  color:#fff;
}
.cl_title{
}
.cl_copy{
  font-size:20px;
  margin: 20px 0;
  display: inline-block;
}
.cl_add{/*the circle*/
  display: inline-block;
  width: 40px;
  height:40px;
  border-radius:50%;
  background-color: #fff;
  cursor: pointer;
  margin:0 0 0 65px;
  color:#c2c2c2;
  padding: 11px 13px;
}
.calendar_events{
  color:$light_grey;
}
.ce_title{
  font-size:14px;
}
.event_item{
  margin: 18px 0;
  padding:5px;
  cursor: pointer;
  &:hover{
    background-image: linear-gradient(-222deg, #FF8494, #FFA9B7);
    box-shadow: 0px 0px 52px -18px rgba(0, 0, 0, 0.75);
    .ei_Dot{
      background-color: #fff;
    }
    .ei_Copy,.ei_Title{
      color:#fff;
    }
  }
}
.ei_Dot,.ei_Title{
  display:inline-block;
}
.ei_Dot{
  border-radius:50%;
  width:10px;
  height: 10px;
  background-color: $light_grey;
  box-shadow: 0px 0px 52px -18px rgba(0, 0, 0, 0.75);
}
.dot_active{
  background-color: #FF8494;
}
.ei_Title{
  margin-left:10px;
  color:#363b41;
}
.ei_Copy{
  font-size:12px;
  margin-left:27px;
}
.dark{
  background-image: linear-gradient(-222deg, #646464, #454545);
  color:#fff;
  .header_title,.ei_Title,.ce_title{
    color:#fff;
  }
}
/* Split the screen in half */
/*
.split {
  height: 100%;
  width: %;
  position: fixed;
  z-index: 1;
  top: 0;
  overflow-x: hidden;
  padding-top: 20px;
}*/
/* Control the left side
.left {
  left: 0;
  background-color: #111;
}*/
/* Control the right side
.right {
  right: 0;
  background-color: red;
}*/
.top_div {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 50%;
    background-color:#F08080;
    text-align:center;
}
.bottom_div {
    position: absolute;
    top: 50%;
    right: 0;
    left: 0;
    bottom: 0;
    background-color:#F0F8FF;
    text-align:center;
    color:#FFFFFF;
}
/* If you want the content centered horizontally and vertically
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}*/
#image {
	display: none;
}
</style>
</head>
<div class="bottom_div">
  <div class="centered">
  
    <div class="container">
    <div class="calendar light">
        <div class="calendar_header">
        <h1 class = "header_title">Lampi Home Security System</h1>
        <p class="header_copy"> Security Alerts</p>
        </div>
        <div class="calendar_plan">
        
        <div class="cl_plan">
            <div class="cl_title">Today</div>
            <div class="cl_copy">
            <p>
                <script> document.write(new Date().toLocaleDateString()); </script>
            </p>
            </div>
            <div class="cl_add">
            <i class="fas fa-plus"></i>
            </div>
        </div>
        </div>

<!-- First SCREENSHOT -->
        <div class="event_item">
              <div class="ei_Dot"></div>
              <div class="ei_Title">
                <p id = "p1></p>
                <script>
                  var today = new Date();
                  var date = (today.getMonth()+1)+'/'+today.getDate()+'/'+today.getFullYear();
                  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
                  var dateTime = date+', '+time;
          document.getElementById("p1").innerHTML = dateTime;
                  </script>
            </div>
          </div>
          <div class="ei_Copy">Movement Detected<br> **Ignored</div>
    <!-- START OF CODE FOR SNAPSHOT BUTTON)-->
            <div>
                <!-- Add id to image -->
                <img id="image" src= "stream2.jpg" 
                    alt="Snapshot image not rendering..." />
            </div>
            <div class="centered">
                <body>
                <!-- <center><h1>Lamp Surveillance Camera Live Stream</h1></center>
                -->
                <center> <img src="stream2.jpg" width="375" height="195"> </center>
            
                </body>
            </div>
            </script>
        </div>

<!-- First SCREENSHOT -->
        <div class="event_item">
              <div class="ei_Dot"></div>
              <div class="ei_Title">
                <p id = "p1></p>
                <script>
                  var today = new Date();
                  var date = (today.getMonth()+1)+'/'+today.getDate()+'/'+today.getFullYear();
                  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
                  var dateTime = date+', '+time;
          document.getElementById("p1").innerHTML = dateTime;
                  </script>
            </div>
          </div>
          <div class="ei_Copy">Movement Detected<br> **Ignored</div>
    <!-- START OF CODE FOR SNAPSHOT BUTTON)-->
            <div>
                <!-- Add id to image -->
                <img id="image" src= "stream3.jpg" 
                    alt="Snapshot image not rendering..." />
            </div>
            <div class="centered">
                <body>
                <!-- <center><h1>Lamp Surveillance Camera Live Stream</h1></center>
                -->
                <center> <img src="stream2.jpg" width="375" height="195"> </center>
            
                </body>
            </div>
            </script>
        </div>

        <center> <img src="stream10.jpg" width="375" height="195"> </center>
<!-- THIRD SCREENSHOT -->
        <div class="event_item">
            <div class="ei_Dot dot_active"></div>
            <div class="ei_Title">Yesterday, 10:30 AM</div>
            <div class="ei_Copy">Loud Sound Detected </div>
        </div>
        <div class="event_item">
            <div class="ei_Dot"></div>
            <div class="ei_Title">April 09, 2022, 12:00 pm</div>
            <div class="ei_Copy">Movement Detected</div>
        </div>
        <div class="event_item">
            <div class="ei_Dot"></div>
            <div class="ei_Title">April 07, 2022, 12:22 pm</div>
            <div class="ei_Copy">Movement Detected</div>
        </div>
        </div>
    </div>
    </div>
  </div>
</div>
<div class="top_div">
  <div class="centered">
    <body>
    <!-- <center><h1>Lamp Surveillance Camera Live Stream</h1></center>
    -->
    <center> <img src="stream.mjpg" width="750" height="390"> </center>
   
    </body>
  </div>
</div>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.snap = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            
            self.buffer.truncate()
            with self.condition:
                self.snap = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self): 
        count = 0 ##number of screenshots taken
        ##a = 0##putting outside of if statements so I can increase it or reference it from within each
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

        elif self.path == '/stream2.jpg':
            print('stream')
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
              
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.snap
                  
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

                    i = GPIO.input(11)  
                    if (i==1):
                      count =1
                      break

                    
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        elif self.path == '/stream3.jpg':
            print('stream')
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
              
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.snap
                  
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

                    time.sleep(5)
                    i = GPIO.input(11)  
                    if (i==1 and count==1):
                      break
                    
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
            
        elif self.path == '/stream.mjpg': ## MAIN STREAM 
            print('stream')
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    # i = GPIO.input(11)
                    # a = 0
                    # # if ( i == 1):
                    # #   if ( a == 0):
                    # #     camera.capture('/home/pi/home-security/pictures/nathanHsiao.jpg')
                    # #   variable = 25
                    # #   print("intruder")

                    # a = 1
                    
                    with output.condition:
                        output.condition.wait()
                        frame = output.snap
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

def load_binary(filename):
    with open(filename, 'rb') as file_handle:
        return file_handle.read()

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

def Send_Email(image):
    sender = 'nathan40241@gmail.com'
    gmail_password = 'Badgebadge29*'
    recipients = ['nnh12@case.edu']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Attachment Test'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = [image]

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise



try:
    time.sleep(2) # to stabilize sensor
    
            
    while True:
        ##Timeloop
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if GPIO.input(23):
            ##If loop
            GPIO.output(24, True)
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
            print("Motion Detected at {}".format(st))
            ##Adds timestamp to image
            camera.capture('image_Time_{}.jpg'.format(st))
            image = ('image_Time_{}.jpg'.format(st))
            Send_Email(image)
            time.sleep(2)
            GPIO.output(24, False)
            time.sleep(5) #to avoid multiple detection

        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()

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
        print("hi")

    finally:
        camera.stop_recording()