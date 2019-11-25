from network import WLAN
from umqtt import MQTTClient
import ubinascii
import machine
import pycom
import time


class adafruit:
    def __init__(self, config, data_collector):
        self.sensor = data_collector
        self.Config = config
        self.AIO_SERVER = config["adafruit"]["AIO_SERVER"]
        self.AIO_PORT = config["adafruit"]["AIO_PORT"]
        self.AIO_USER = config["adafruit"]["AIO_USER"]
        self.AIO_KEY = config["adafruit"]["AIO_KEY"]
        self.AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
        self.AIO_CONTROL_FEED = config["adafruit"]["AIO_CONTROL_FEED"]
        self.AIO_RANDOMS_FEED = config["adafruit"]["AIO_RANDOMS_FEED"]
        self.last_random_sent_ticks = config["adafruit"]["last_random_sent_ticks"]

        """Finding and connecting to network"""
        wlan = WLAN(mode=WLAN.STA)
        nets = wlan.scan()
        print("Scanning for Wifi")
        for net in nets:
            for knowNet in self.Config["network"]:
                if net.ssid == knowNet["name"]:
                    print(net.ssid + ' found!')
                    wlan.connect(net.ssid, auth=(net.sec, knowNet["password"]), timeout=5000)
                    while not wlan.isconnected():
                        machine.idle() # save power while waiting
                    print('WLAN connection succeeded!')
                    break


    def runAdafruit(self):
        #Uses the MQTT protocol to connect to Adafruit IO
        client = MQTTClient(self.AIO_CLIENT_ID, self.AIO_SERVER, self.AIO_PORT, self.AIO_USER, self.AIO_KEY)

        #Subscribed messages will be delivered to this callback
        client.set_callback(self.sub_cb)
        client.connect()
        client.subscribe(self.AIO_CONTROL_FEED)
        print("Connected to %s, subscribed to %s topic" % (self.AIO_SERVER, self.AIO_CONTROL_FEED))

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
        if ((time.ticks_ms() - self.last_random_sent_ticks) < 2000):
            return;

        angle = self.sensor.getAngle()
        velocity = self.sensor.getVelocity()
        print("Publishing: {0} to {1} ... ".format(angle, self.AIO_RANDOMS_FEED), end='')
        try:
            client.publish(topic=self.AIO_RANDOMS_FEED, msg=str(angle))
            print("DONE")
        except Exception as e:
            print("FAILED")
        finally:
            self.last_random_sent_ticks = time.ticks_ms()
