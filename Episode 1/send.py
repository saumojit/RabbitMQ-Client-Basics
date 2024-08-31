#!/usr/bin/env python
import pika

# Connecting to Broker On LocalHost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Creating Queue
channel.queue_declare(queue='hello')

# Message Published through Default-Exchange (X) to The Queue ( Not Directly to The Queue )
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [X] Sent 'Hello World!'")
# RabbitMQ WebConsole ==> http://localhost:15672/#/

#Making Sure that Flushing Network Buffers and Message Delivered

connection.close()