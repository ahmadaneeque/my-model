import os
import pika
import time

rabbit_host = os.getenv("RABBIT_HOST",'rabbit')
rabbit_port = os.getenv("RABBIT_PORT", 5672) 
rabbit_user = os.getenv("RABBIT_USERNAME", 'guest')
rabbit_password = os.getenv("RABBIT_PASSWORD", 'guest') 

credentials = pika.PlainCredentials(rabbit_user, rabbit_password)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, credentials=credentials))
channel = connection.channel()

# channel.queue_declare(queue='hello')  for single message consumer  will not be created for multiple consumers here
channel.exchange_declare(exchange='logs', exchange_type='fanout')  # for multiple consumer of same message

sleepTime = 2
count = 0

while True:
   message = 'Hello World! %s'% count
#   channel.basic_publish(exchange='', routing_key='hello', body=message)  #for single consumer of message 
   channel.basic_publish(exchange='logs', routing_key='', body=message)   # for multiple consumer of same message

   count+=1	
   print(" [x] Sent 'Hello World!'")

   time.sleep(sleepTime)

connection.close()
