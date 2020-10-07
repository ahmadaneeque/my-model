#!/usr/bin/env python
import pika, sys, os


rabbit_host = os.getenv("RABBIT_HOST")
rabbit_port = os.getenv("RABBIT_PORT") 
rabbit_user = os.getenv("RABBIT_USERNAME")
rabbit_password = os.getenv("RABBIT_PASSWORD")  


credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(
		host=rabbit_host, port=rabbit_port, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

#binding_keys = sys.argv[1:]
binding_keys = ["kern.*"]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
