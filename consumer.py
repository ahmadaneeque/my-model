#!/usr/bin/env python
import pika, sys, os

rabbit_host = os.getenv("RABBIT_HOST",'rabbit')
rabbit_port = os.getenv("RABBIT_PORT", 5672) 
rabbit_user = os.getenv("RABBIT_USERNAME", 'guest')
rabbit_password = os.getenv("RABBIT_PASSWORD", 'guest')  


def main():
    credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, credentials=credentials))

    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')    # for multiple consumer of same message

    result = channel.queue_declare(queue='', exclusive=True)   # create a queue exclusively for this consumer
  #  channel.queue_declare(queue='hello') # for single message consumer

    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

  #  channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True) 
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
