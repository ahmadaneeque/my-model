import os
import pika
import time

rabbit_host = os.getenv("RABBIT_HOST")
rabbit_port = os.getenv("RABBIT_PORT") 
rabbit_user = os.getenv("RABBIT_USERNAME")
rabbit_password = os.getenv("RABBIT_PASSWORD") 

credentials = pika.PlainCredentials(rabbit_user, rabbit_password)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

sleepTime = 1
count = 0

while True:

	routing_key = 'kern.cons'
	message = 'Hello World! %s'% count
	channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
	print(" [x] Sent %r:%r" % (routing_key, message))
	time.sleep(sleepTime)
	
	routing_key = 'topic2'
	message = 'kernal hello %s'% count
	channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
	print(" [x] Sent %r:%r" % (routing_key, message))

	count+=1	
	time.sleep(sleepTime)

connection.close()
