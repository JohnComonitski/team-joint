import machine
import json
import utime
from machine import RTC

#Setting up RTC
rtc = RTC()
rtc.init((2014, 5, 1, 4, 13, 0, 0, 0),RTC.INTERNAL_RC)

#Stoping Blinking
pycom.heartbeat(False)

"""creating Config object"""
class Config(object):
    def __init__(self):
        try:
            with open('config.json', encoding='utf-8') as config:
                self.__dict__ = json.load(config)
        except (OSError, IOError) as e:
            print("Could not load config", e)
config = Config().__dict__

sensors = dataCollector()
mode = config["mode"]
#The device has different modes found in config.json
#Mode: "write" prints to disk
#Mode: "adafruit" publishes to adafruitIO
if(mode == "write"):
    Writer = writer(config, sensors)
    Writer.runWriter()
elif(mode == "adafruit"):
    Adafruit = adafruit(config, sensors)
    Adafruit.runAdafruit()
