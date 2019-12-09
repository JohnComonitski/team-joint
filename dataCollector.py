import math
import pycom
import time
from LIS2HH12 import LIS2HH12
from L76GNSS import L76GNSS
from pytrack import Pytrack
from pycoproc import Pycoproc
import gc
import utime

class dataCollector:
    def __init__(self, logger):
        gc.enable()
        self.acc = LIS2HH12(pysense = None, sda = "P22", scl = "P21")
        py = Pytrack()
        self.gps = L76GNSS(py, timeout=30)
        self.py = Pycoproc()
        self.batteryTrack = 0
        self.Logger = logger


    #These two methods call the accelerometer and collect data
    def getAngle(self):
        return self.acc.roll() + 180

    def getAcceleration(self):
        accel = self.acc.acceleration()
        return accel

    def getGPS(self):
        return self.gps.coordinates()

    def checkBatt(self):
        volt = self.py.read_battery_voltage()
        percentage = volt/3.7
        if(percentage < .10 and self.batteryTrack == 3):
            Time = utime.localtime(None)
            currentTime = str(Time[1]) + "/"  + str(Time[2]) + "/" + str(Time[0]) + " at " + str(Time[3]) + ":" + str(Time[4]) + ":" + str(Time[5])
            self.Logger.log("Battery life critically low at " + str(percentage*100) + "% at " + currentTime)
            self.batteryTrack+=1
        elif(percentage < .25 and self.batteryTrack == 2):
            self.Logger.log("Battery life at " + str(percentage*100) +"%")
            self.batteryTrack+=1
        elif(percentage < .5 and self.batteryTrack == 1):
            self.Logger.log("Battery life at " + str(percentage*100) +"%")
            self.batteryTrack+=1
        elif(percentage <.75 and self.batteryTrack == 0):
            self.Logger.log("Battery life at " + str(percentage*100) +"%")
            self.batteryTrack+=1
