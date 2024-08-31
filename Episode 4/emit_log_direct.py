#!/usr/bin/env python
import pika
import sys

#Connection
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()

#Exchange
channel.exchange_declare(exchange='logs_direct' , exchange_type='direct')

#Severity Input which will act as routing key
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

#message
message = ' '.join(sys.argv[2:]) or 'Hello World!'

#Channel to Publish the body with the routing key to the Exchange
channel.basic_publish(exchange='direct_logs',routing_key=severity, body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()
