#!/usr/bin/env python
import pika
import sys
from os import getenv

rabbit_service_name = getenv("RABBIT_SVC")
rabbit_namespace = getenv("RABBIT_NAMESPACE")
domain = getenv("DOMAIN")
rabbit_port = getenv("RABBIT_PORT")

rabbit_user = getenv("RABBIT_USERNAME")
rabbit_password = getenv("RABBIT_PASSWORD")

rabbit_host = '%s.%s.svc.%s' % (rabbit_service_name, rabbit_namespace, domain)
credentials = pika.PlainCredentials(rabbit_user, rabbit_password)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, credentials=credentials))
except Exception as e:
    raise e


channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# binding_keys = sys.argv[1:]
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
