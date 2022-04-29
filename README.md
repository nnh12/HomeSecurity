# HomeSecurity
This is our home secuity system that is operated by a controlled by a Rasyberry Pi 4. To launch the program, you will need to run **main.py.** This file contains all the necessary code to run the webserver. 

This home security system will include the following:  **(1)** a live stream survelliance camera hosted a webserver, **(2)** a motion detection system that simultaneously captures a photo, **(3)** and an email notification system that will deliver the captured photo asynchronously. 

For hardware, we soldered and coonected the Raspyberry Pi Camera and a PIR motion sensor the Pi's GPIO Pin 17 for external communication.

Frameworks and Libraries Used
---
For the webserver, we will be using the SocketServer framework to handle incoming requests into the server's address. We will then be using python's Threading library to asynchronously update the video simultaneously. We used the SMTP protocol client to create an object that can be used to send mail to any internet machine with an SMTP listener daemon. Finally, we used the Raspberry pi's built-in Picamera library to access the photos/live stream.
