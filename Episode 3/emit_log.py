#!/usr/bin/env python
import pika
import sys

# Connecting to RabbitMQ Server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Creating Exchange(X) with Type as Fanout
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# Publishing Messages to The Exchange , Routing Key won't be needed , as it will be broadcast
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()