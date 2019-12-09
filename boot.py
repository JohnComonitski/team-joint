from network import WLAN
import machine
from machine import SD
import os
import json
import time
import utime
from machine import RTC
import pycom
from dataCollector import dataCollector
from writer import writer
from adafruit import adafruit
from logger import logger
from encrypt import encrypt

#pycom.rgbled(0xFF0000)  # Red
#pycom.rgbled(0x0000FF)  # Blue
"""Stoping Blinking"""
pycom.heartbeat(False)

"""Setting up SD Card"""
sd = SD()
os.mount(sd, '/sd')

"""Creating Logger"""
Logger = logger()

Logger.log("---------------------")
Logger.log("Creating new session.")
Logger.log("---------------------")


"""creating Config object"""
class Config(object):
    def __init__(self):
        try:
            with open('config.json', encoding='utf-8') as config:
                self.__dict__ = json.load(config)
        except (OSError, IOError) as e:
            Logger.log("Error: Could not load config" + str(e))
config = Config().__dict__


"""Setting up Time"""
rtc = machine.RTC()
Logger.log("Syncing Clock. Attempting to find network")
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
Logger.log("Scanning for Wifi")
for net in nets:
    for knowNet in config["network"]:
        if net.ssid == knowNet["name"]:
            Logger.log(net.ssid + ' found!')
            wlan.connect(net.ssid, auth=(net.sec, knowNet["password"]), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            Logger.log('WLAN connection succeeded!')
            rtc.ntp_sync("pool.ntp.org")
            break
time.sleep(10)

sensors = dataCollector(Logger)
encryption = encrypt(config, logger)
mode = config["mode"]
Logger.log("Begining session with mode: " + mode)

#The device has different modes found in config.json
#Mode: "write" prints to disk
#Mode: "Ewrite" prints encrypted data to disk
#Mode: "adafruit" publishes to adafruitIO
#Mode: "decrypt" Will decrypt any data
if(mode == "write"):
    Writer = writer(config, sensors, wlan, logger, encryption)
    Writer.runWriter()
if(mode == "Ewrite"):
    Writer = writer(config, sensors, wlan, logger, encryption)
    Writer.runEWriter()
elif(mode == "adafruit"):
    Adafruit = adafruit(config, sensors, logger)
    Adafruit.runAdafruit()
elif(mode == "decrypt"):
    try:
        f = open("/sd/private.pem")
        pycom.rgbled(0xFF0000)  # Red
        encryption.RSADecrypt(f)
        pycom.rgbled(0x0000FF)  # Blue
    except IOError:
        Logger.log("Error: Could not find file \'private.pem\'")
    finally:
        f.close()
