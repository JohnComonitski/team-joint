import pycom
import time
import utime
from encrypt import encrypt


class writer:
    def __init__(self, config, data_collector, wlan, logger, encryption):
        self.sensor = data_collector
        self.Encryption = encryption
        self.wifi = wlan
        self.Logger = logger
        self.Frequency = config["frequency"]

        #Preping to file
        f = open('/sd/moveData.txt', 'w')
        f.close()

    def runWriter(self):
        self.wifi.disconnect()
        Time = utime.localtime(None)
        startTime = str(Time[1]) + "/"  + str(Time[2]) + "/" + str(Time[0]) + " at " + str(Time[3]) + ":" + str(Time[4]) + ":" + str(Time[5])
        self.Logger.log("Session began at " + startTime)

        pycom.rgbled(0x00FF00)  # Green
        while True:
            time.sleep(1/self.Frequency)

            self.sensor.checkBatt()

            angle = str(self.sensor.getAngle())
            coords = self.sensor.getGPS()
            Time = utime.localtime(None)
            currentTime = str(Time[1]) +"-"+ str(Time[2]) +"-"+ str(Time[0]) +"-" +str(Time[3])+":"+str(Time[4])+":"+str(Time[5])

            data = currentTime + "," + angle + "," + str(coords[0]) + "," + str(coords[1])
            f = open('/sd/moveData.txt', 'a')
            f.write(data + "\n")
            f.close()

    def runEWriter(self):
        self.wifi.disconnect()
        Time = utime.localtime(None)
        startTime = str(Time[1]) + "/"  + str(Time[2]) + "/" + str(Time[0]) + " at " + str(Time[3]) + ":" + str(Time[4]) + ":" + str(Time[5])
        self.Logger.log("Session began at " + startTime)

        pycom.rgbled(0x00FF00)  # Green
        while True:
            time.sleep(1/self.Frequency)

            self.sensor.checkBatt()

            angle = str(self.sensor.getAngle())
            coords = self.sensor.getGPS()
            Time = utime.localtime(None)
            currentTime = str(Time[1]) +"-"+ str(Time[2]) +"-"+ str(Time[0]) +"-" +str(Time[3])+":"+str(Time[4])+":"+str(Time[5])

            data = currentTime + "," + angle + "," + str(coords[0]) + "," + str(coords[1])
            msg = self.EncryptSion.RSAEncrypt(data)
            f = open('/sd/EMoveData.txt', 'a')
            f.write(msg + "\n")
            f.close()
