# Patrick McCorkell
# February 2021
# US Naval Academy
# Robotics and Control TSD
#


import os
import ujson
from machine import reset,Pin,ADC,PWM
try:
  from machine import SoftI2C as I2C
except:
  from machine import I2C
from time import sleep
from ubinascii import hexlify
from gc import collect as trash


#Define function to reload modules
#dhylands and solarkraft on micropython forums:
#     https://forum.micropython.org/viewtopic.php?f=2&t=413&sid=c23da3aea8b3f4dbdd8bb29abcb1a09c&start=30
def reload(mod):
	import sys
	mod_name = mod.__name__
	del sys.modules[mod_name]
	__import__(mod.__name__)
	print('reloaded '+mod_name)

# A basic loop for reading ADC on pin 36.
def adc_loop(time=0.001,length=1,verbose=0):
	adc=ADC(Pin(36))
	adc.atten(3)
	print("read adc from pin 36")
	results=[]
	x=length/time
	i=0
	while(i<x):
		val=adc.read()
		if (verbose==1):
			print(val)
		results.append(val)
		i+=1
		sleep(time)
	return results;

# A basic loop for reading DigitalIn on pin 36
def dig_loop(time=0.001,length=1,verbose=0):
	digital=Pin(36,Pin.IN)
	print("read digital from pin 36")
	results=[]
	x=length/time
	i=0

	while(i<x):
		val=digital.value()
		if (verbose==1):
			print(val)
		results.append(val)
		i+=1
		sleep(time)
	return results;

# Logfile functionality.
# Consider using one of the "loops" above, or some other function as the 'data' object.
def log(data,filename='logfile'):
	f = open(filename,'w')
	f.write(ujson.dumps(data))
	f.close()


#########################
### DEFAULT I2C SETUP ###
#########################

#Read and Write functions use unsigned integers. Check your data sheet if twos_comp or the like is needed.

# i2c setup

# Heltec OLED i2c pins
#SCL=Pin(15)
#SDA=Pin(4)

# Adafruit Feather i2c pins
SCL=Pin(22)
SDA=Pin(23)	
i2c = I2C(sda=SDA,scl=SCL)

# Tell us the address of every device connected to I2C.
def scan_i2c():
	scan = i2c.scan()
	scan_string="i2c scan: "
	for i in scan:
		scan_string+=((hex(i))+"  ")
	print(scan_string)
	print()

scan_i2c()

#Write an unsigned int to an i2c register. Reads the register back and returns it's value as an unsigned integer.
def i2c_write(address,register,value):
	i2c.writeto_mem(address,register,bytearray([value]))
	return i2c_read_H(address,register,1)

#read i2c register(s) in big endian. Returns unsigned integer. 
def i2c_read_H(address,register,length):
	#read the register(s) into a bytearray
	bytedata=i2c.readfrom_mem(address,register,length)
	returnval=0
	i=0
	while (i<length):
		returnval+=(bytedata[i]<<(8*(length-i-1)))
		i+=1
	return returnval

#read i2c register(s) in little endian. Returns unsigned integer.
def i2c_read_L(address,register,length):
	#read the register(s) into a bytearray
	bytedata=i2c.readfrom_mem(address,register,length)
	returnval=0
	#iterate through the bytearray and store as unsigned int
	i=length-1
	while(i>=0):
		returnval+=(bytedata[i]<<(8*i))
		i-=1
	return returnval

try:
  wlan0.connect('SURF','12345678')
  # wlan0.connect('GNBA-F')
except:
  print('wifi error')
