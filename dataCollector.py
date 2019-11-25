import math
import pycom
import time
from LIS2HH12 import LIS2HH12

class dataCollector:
    def __init__(self):
        self.acc = LIS2HH12(pysense = None, sda = "P22", scl = "P21")

    #These two methods call the accelerometer and collect data
    def getAngle():
        return self.acc.roll() + 180

    def getVelocity():
        accel = self.acc.acceleration()
        ax = accel[0]*accel[0]
        ay = accel[1]*accel[1]
        az = accel[2]*accel[2]
        print(str(ax) + "  " + str(ay) + "  " + str(az))
        return (math.sqrt(ax + ay + az))
