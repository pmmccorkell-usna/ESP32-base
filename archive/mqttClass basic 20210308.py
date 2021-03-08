from ubinascii import hexlify
from machine import unique_id
from umqttsimple import MQTTClient
from time import sleep
from random import randint


class mqttClass:
	# Initial setup
	def __init__(self,hostIP,port=0,user=b'username',password=b'password'):
		self.mqtt_server=hostIP
		# self.client_id=hexlify(unique_id()+str(randint(1000,9999)))
		self.client_id = str(randint(1000,9999))
		# port=0
		# user=b'username'
		# password=b'password'
		#mqtt=MQTTClient(client_id,mqtt_server,port,user,password)
		self.mqtt=MQTTClient(self.client_id,self.mqtt_server)

		#Array of topics currently subscribed to.
		self.topic_list=set()

		# Dictionary
		self.topic_outsourcing={
			# insert topic(s) as key, and function location as value
			'test':self.test,
			'default':self.defaultFunction
		}
		self.mqtt.set_callback(self.trigger)
		#self.connect()

	def test(self,top,msg):
		print()
		print("test topic rx")
		print(top)
		print(msg)
		print()

	# Redirect from MQTT callback function.
	# Error checking.
	def defaultFunction(self,top,msg):
		print("PYTHON >> Discarding. No filter for topic "+str(top)+" discovered.")
		print("PYTHON >> Discarded data: "+str(msg))


	#When a message is received, this function is called.
	def trigger(self,bytes_topic,bytes_msg):
		#Format the data into variables that are python friendly
		topic=bytes_topic.decode()
		#print(topic)
		message = bytes_msg.decode()
		#val=float(msg)
		#print(val)
		topicFunction=self.topic_outsourcing.get(topic,self.defaultFunction)
		topicFunction(topic,message)
		return self.update()


	#Connect and maintain MQTT connection to Home Assistant
	def reconnect(self):
		print("Dropped mqtt connection. Reconnecting")
		sleep(2)
		self.connect()
	def connect(self):
		try:
			self.mqtt.connect()
		except OSError as e:
			self.reconnect()
		return 1

	#Publish to a topic
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

	#Setup subscription to a topic
	def sub(self,topic):
		self.topic_list.add(topic)
		self.mqtt.subscribe(topic)

	#Look for new messages on subscribed topics from Home Assistant.
	def update(self):
		self.mqtt.check_msg()
