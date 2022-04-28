
''''
import paho.mqtt.client as mqtt
import base64

client=mqtt.Client()
client.connect('mqtt.eclipseprojects.io')
client.subscribe("topic")

with open("/home/pi/home-security/pictures/nathanHsiao.jpg", "rb") as image:
    img = image.read()

message = img
base64_bytes = base64.b64encode(message)
base64_message = base64_bytes.decode('ascii')

client.publish('topic', base64_message)
'''
''''
import paho.mqtt.publish as publish
MQTT_SERVER = "172.19.91.92"  #Write Server IP Address
MQTT_PATH = "Image"

a = " hi"
f=open("/home/pi/home-security/pictures/nathanHsiao.jpg", "rb") #3.7kiB in same folder
fileContent = f.read()
byteArr = bytearray(fileContent)


publish.single(MQTT_PATH, "hi")
'''
import paho.mqtt.client as MQTT
c = MQTT.Client()
c.enable_logger()
c.connect('localhost', port=1883, keepalive=60)
c.loop_start()
c.publish('hello', 'world')