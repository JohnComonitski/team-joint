"""
from network import WLAN
from umqtt import MQTTClient
import ubinascii
import machine
import math
import micropython
import pycom
import time
from LIS2HH12 import LIS2HH12
from machine import SD
import os





#Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "TeamJoint"
AIO_KEY = "a5ec61d4fa7c457c8b6829041443db13"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
AIO_CONTROL_FEED = "TeamJoint/feeds/lights"
AIO_RANDOMS_FEED = "TeamJoint/feeds/movement"
last_random_sent_ticks = 0  # milliseconds

#Setting up SD Card
sd = SD()
sd.init()
os.mount(sd, '/sd')

#Signal start#
pycom.rgbled(0x0000FF)  # Blue
time.sleep(1)
pycom.rgbled(0xFF0000)  # Red
time.sleep(1)
pycom.rgbled(0x0000FF)  # Blue


#Preping to file
f = open('/sd/moveData.txt', 'w')
f.close()

#activate accelerometer
acc = LIS2HH12(pysense = None, sda = "P22", scl = "P21")


#responds to messages from Adafruit IO
def sub_cb(topic, msg):
    print((topic, msg))
    if msg == b"ON":
        pycom.rgbled(0xffffff)
    elif msg == b"OFF":
        pycom.rgbled(0x000000)
    else:
        print("Unknown message")

#These two methods call the accelerometer and collect data
def getAngle():
    return acc.roll() + 180

def getVelocity():
    accel = acc.acceleration()
    ax = accel[0]*accel[0]
    ay = accel[1]*accel[1]
    az = accel[2]*accel[2]
    print(str(ax) + "  " + str(ay) + "  " + str(az))
    return (math.sqrt(ax + ay + az))
#Sends messages to Adafuit IO
def sendMovement():
    global last_random_sent_ticks

    #Waits 2 seconds to send data to avoid Adadruit IO
    if ((time.ticks_ms() - last_random_sent_ticks) < 2000):
        return;

    angle = getAngle()
    velocity = getVelocity()
    print("Publishing: {0} to {1} ... ".format(angle, AIO_RANDOMS_FEED), end='')
    try:
        client.publish(topic=AIO_RANDOMS_FEED, msg=str(angle))
        print("DONE")
    except Exception as e:
        print("FAILED")
    finally:
        last_random_sent_ticks = time.ticks_ms()

#Uses the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

#Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_CONTROL_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_CONTROL_FEED))

#Changes light to green to indicate connected to Adafruit
pycom.rgbled(0x00ff00)

try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    while 1:              # Repeat this loop forever
        client.check_msg()# Action a message if one is received. Non-blocking.
        sendMovement()     # Send a random number to Adafruit IO if it's time.
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    wlan.disconnect()
    wlan = None
    pycom.rgbled(0x000022)# Status blue: stopped
    print("Disconnected from Adafruit IO.")

#This code is commented out and used to write data to the sd Card
while True:
    #pycom.rgbled(0xFF0000)  # Red
    time.sleep(.25)

    angle = str(acc.roll())
    acceleration = acc.acceleration()
    currentTime = str(time.time())

    data = currentTime + "," + angle + "," + str(acceleration[0]) + "," + str(acceleration[1]) + "," + str(acceleration[2]) +"\n"
    f = open('/sd/moveData.txt', 'a')
    f.write(data)
    f.close()
    #pycom.rgbled(0x00FF00)  # Green
"""
