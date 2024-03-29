from network import WLAN
from umqtt import MQTTClient
import ubinascii
import machine
import pycom
import time
import utime


class adafruit:
    def __init__(self, config, data_collector, logger):
        self.sensor = data_collector
        self.Config = config
        self.Logger = logger
        self.AIO_SERVER = config["adafruit"]["AIO_SERVER"]
        self.AIO_PORT = config["adafruit"]["AIO_PORT"]
        self.AIO_USER = config["adafruit"]["AIO_USER"]
        self.AIO_KEY = config["adafruit"]["AIO_KEY"]
        self.AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
        self.AIO_CONTROL_FEED = config["adafruit"]["AIO_CONTROL_FEED"]
        self.AIO_MOVEMENT_FEED = config["adafruit"]["AIO_MOVEMENT_FEED"]
        self.AIO_GPS_FEED = config["adafruit"]["AIO_GPS_FEED"]
        self.AIO_ACCELERATION_FEED = config["adafruit"]["AIO_ACCELERATION_FEED"]
        self.last_random_sent_ticks = config["adafruit"]["last_random_sent_ticks"]
        self.post_per_minute = config["adafruit"]["post_per_minute"]

        """Finding and connecting to network"""
        self.wlan = WLAN(mode=WLAN.STA)
        nets = self.wlan.scan()
        print("Scanning for Wifi")
        for net in nets:
            for knowNet in self.Config["network"]:
                if net.ssid == knowNet["name"]:
                    print(net.ssid + ' found!')
                    self.wlan.connect(net.ssid, auth=(net.sec, knowNet["password"]), timeout=5000)
                    while not self.wlan.isconnected():
                        machine.idle() # save power while waiting
                    print('WLAN connection succeeded!')
                    break

        self.client = MQTTClient(self.AIO_CLIENT_ID, self.AIO_SERVER, self.AIO_PORT, self.AIO_USER, self.AIO_KEY)



    def runAdafruit(self):
        Time = utime.localtime(None)
        currentTime = str(Time[1]) + "/"  + str(Time[2]) + "/" + str(Time[0]) + " at " + str(Time[3]) + ":" + str(Time[4]) + ":" + str(Time[5])
        self.Logger.log("Session began at " + currentTime)
        #Subscribed messages will be delivered to this callback
        self.client.set_callback(self.sub_cb)
        print('Connecting to io.adafruit.com')
        time.sleep(10)
        self.client.connect()
        self.client.subscribe(self.AIO_CONTROL_FEED)
        print("Connected to %s, subscribed to %s topic" % (self.AIO_SERVER, self.AIO_CONTROL_FEED))


        pycom.rgbled(0x0000FF)  # Blue

        try:
            while 1:
                self.client.check_msg()
                self.sendMovement()
        finally:
            self.client.disconnect()
            self.client = None
            self.wlan.disconnect()
            self.wlan = None
            pycom.rgbled(0x000022)
            print("Disconnected from Adafruit IO.")

    #responds to messages from Adafruit IO
    def sub_cb(self, topic, msg):
        print((topic, msg))
        if msg == b"ON":
            pycom.rgbled(0xffffff)
        elif msg == b"OFF":
            pycom.rgbled(0x000000)
        else:
            print("Unknown message")

    #Sends messages to Adafuit IO
    def sendMovement(self):
        #Waits 2 seconds to send data to avoid Adadruit IO
        if ((time.ticks_ms() - self.last_random_sent_ticks) < (1000/(self.post_per_minute)/60)):
            return;

        angle = self.sensor.getAngle()
        acceleration = self.sensor.getAcceleration()
        gps = self.sensor.getGPS()
        if(str(gps[0]) == "None"):
            gps = "0,40.808679,-77.855693,0"
        else:
            gps = "0,"+str(gps[0])+","+str(gps[1])+",0"


        print("Publishing: {0} to {1}, {2} to {3}, {4} to {5} ... ".format(angle, self.AIO_MOVEMENT_FEED,acceleration, self.AIO_ACCELERATION_FEED,gps, self.AIO_GPS_FEED), end='')
        try:
            self.client.publish(topic=self.AIO_MOVEMENT_FEED, msg=str(angle))
            self.client.publish(topic=self.AIO_ACCELERATION_FEED, msg=str(acceleration))
            self.client.publish(topic=self.AIO_GPS_FEED, msg=str(gps))
            print("DONE")
        except Exception as e:
            print(e)
            print("FAILED")
        finally:
            self.last_random_sent_ticks = time.ticks_ms()
