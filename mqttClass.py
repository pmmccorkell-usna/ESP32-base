#
# Streamlined class of umqttsimple for micropython
# US Naval Academy
# Robotics and Control TSD
# Patrick McCorkell
# March 2021
#

from ubinascii import hexlify
from machine import unique_id, Timer
from umqttsimple import MQTTClient
from time import sleep
from random import randint


#USAGE:
# from mqttClass import mqttClass
#
# server = 'the broker's IP'
# mqtt = mqttClass(server)
#      if connecting to Adafruit IO or 3rd party with username and pass:
#           mqtt = mqttClass(server, username='YOUR IO USER', password='YOUR IO KEY')
# mqtt.connect()
# 
# To Publish:
# mqtt.pub('topic','message')
#
# To Subscribe:
# def yourFunction(topic,message):
#     ......
#     your code for subscription
#     ......
#
# mqtt.topic_outsourcing['your Topic'] = yourFunction
# mqtt.sub('your Topic')
# # mqtt.update() must be used within the main loop to check for new messages on 'your Topic'.
#

class mqttClass:
	# Initial setup
	def __init__(self,hostIP,username=None,password=None,subscriptions=None,interval=100,timer_n=1):
		self.mqtt_server=hostIP
		# self.client_id=hexlify(unique_id()+str(randint(1000,9999)))
		self.client_id = str(randint(1000,9999))
		port=1883
		# user=b'username'
		# password=b'password'
		#mqtt=MQTTClient(client_id,mqtt_server,port,user,password)
		self.mqtt=MQTTClient(self.client_id,self.mqtt_server,port,username,password)

		self.update_timer = Timer(timer_n)
		self.timer_rate = interval

		#Array of topics currently subscribed to.
		self.topic_list=set()

		self.mqtt.set_callback(self.trigger)

		topic_defaults={
			# insert topic(s) as key, and function location as value
			'test':self.test,
			'default':self.defaultFunction
		}

		# Dictionary to associate subscription topics to their function()
		if type(subscriptions) is dict:
			print("registered subscription dictionary")
			self.topic_outsourcing = subscriptions
			# self.auto_subscribe()
			
			# self.topic_outsourcing['default'] = self.defaultFunction
		else:
			self.topic_outsourcing = topic_defaults


		#self.connect()

	def auto_subscribe(self):
		# print(self.topic_outsourcing)
		for k in self.topic_outsourcing:
			# print(k)
			self.sub(k)

	# For topic 'test', print out the topic and message
	def test(self,top,msg):
		print()
		print("test topic rx")
		print(top)
		print(msg)
		print()

	# Redirect from MQTT callback function.
	# Error checking.
	def defaultFunction(self,top,msg):
		print("Discarding. No filter for topic "+str(top)+" discovered.")
		print("Discarded data: "+str(msg))


	#When a message is received, this function is called.
	def trigger(self,bytes_topic,bytes_msg):
		# Format the data into variables that are python friendly.
		topic=bytes_topic.decode()
		message = bytes_msg.decode()
		# Locate the function for the incoming topic. If not found, use the defaultFunction.
		topicFunction=self.topic_outsourcing.get(topic,self.defaultFunction)
		topicFunction(topic,message)
		#return self.update()


	#Connect and maintain MQTT connection to Home Assistant
	def reconnect(self):
		print(self.mqtt_server+" dropped mqtt connection. Reconnecting")
		sleep(2)
		self.connect()
	def connect(self):
		try:
			self.mqtt.connect()
			print("Connected to "+self.mqtt_server)
		except OSError as e:
			self.reconnect()
		self.auto_subscribe()
		self.update_timer.init(mode=Timer.PERIODIC,period=self.timer_rate, callback=self.update_callback)
		return 1

	# Publish to a topic.
	def pub(self,topic,message):
	#	print("topic: "+topic)
	#	print("message: "+str(message))
		sent=0
		while (sent<100):
			try:
				self.mqtt.publish(topic,str(message))
	#			print("checks in the mail")
				sent=9000
			except OSError as e:
				self.mqtt.connect()
				print("mqtt dropped " + str(sent) + "times")
				sent+=1
				sleep(0.1)

	# Setup subscription to a topic.
	def sub(self,topic):
		self.topic_list.add(topic)
		self.mqtt.subscribe(topic)

	# Look for new messages on subscribed topics.
	def update_callback(self,event=None):
		try:
			self.mqtt.check_msg()
		except:
			print('ERROR: '+self.mqtt_server+' failed callback.')
			print("Quitting timer callback. Restart subscriptions.")
			self.update_timer.deinit()
			self.connect()

	def update(self):
		self.mqtt.check_msg()

	def __str__(self):
		return str(self.mqtt_server)