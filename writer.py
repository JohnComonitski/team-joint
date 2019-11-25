from machine import SD
import os
import pycom
import time

class writer:
    def __init__(self, config, data_collector):
        self.sensor = data_collector
        #Setting up SD Card
        sd = SD()
        sd.init()
        os.mount(sd, '/sd')
        #Preping to file
        f = open('/sd/moveData.txt', 'w')
        f.close()

    def runWriter(self):
        while True:
            #pycom.rgbled(0xFF0000)  # Red
            time.sleep(.25)

            angle = str(self.sensor.roll())
            acceleration = self.sensor.acceleration()
            currentTime = str(time.time())

            data = currentTime + "," + angle + "," + str(acceleration[0]) + "," + str(acceleration[1]) + "," + str(acceleration[2]) +"\n"
            f = open('/sd/moveData.txt', 'a')
            f.write(data)
            f.close()
            #pycom.rgbled(0x00FF00)  # Green
