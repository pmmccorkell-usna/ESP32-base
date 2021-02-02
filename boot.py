# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
webrepl.start()
from time import sleep

try:
    import usocket as socket
except:
    import socket

#Import the GPIO pins
from machine import Pin

import esp
esp.osdebug(None)

#garbage collection
from gc import collect
collect()

#Setup our wifi network
import network
import ubinascii
print(ubinascii.hexlify(network.WLAN().config('mac'),':').decode())

wlan0 = network.WLAN(network.STA_IF)
wlan0.active(True)



