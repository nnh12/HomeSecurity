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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

camera = PiCamera()


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

.container{
  margin:100px auto;
  width:809px;
}

.light{
  background-color: #fff;
}
.dark{
  margin-left: 65px;
}

.calendar{
  width:370px;
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
.cl_plan{
  width:100%;
  height: 140px;
  background-image: linear-gradient(-222deg, #FF8494, #ffa9b7);
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

.cl_add{
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
    background-image: linear-gradient(-222deg, #FF8494, #ffa9b7);
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
.split {
  height: 100%;
  width: 50%;
  position: fixed;
  z-index: 1;
  top: 0;
  overflow-x: hidden;
  padding-top: 20px;
}

/* Control the left side */
.left {
  left: 0;
  /*background-color: #111;*/
}

/* Control the right side */
.right {
  right: 0;
  /*background-color: red;*/
}

/*
/* If you want the content centered horizontally and vertically */
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
*/

</style>

</head>

<div class="split left">
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
        <div class="calendar_events">
        <p class="ce_title">Previous Alerts</p>
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
            <div class="ei_Title">April 08, 2022, 12:00 pm</div>
            <div class="ei_Copy">Movement Detected<br> **Ignored</div>
        </div>
        <div class="event_item">
            <div class="ei_Dot"></div>
            <div class="ei_Title">April 07, 2022, 12:22 pm</div>
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

<div class="split right">
  <div class="centered">

    <body>

    <!-- <center><h1>Lamp Surveillance Camera Live Stream</h1></center>
    -->

    <center> <img src="stream.mjpg" width="1500" height="780"> </center>
    </body>

  </div>
</div>
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

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
