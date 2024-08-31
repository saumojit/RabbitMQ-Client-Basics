#!/usr/bin/env python
# python receive_logs.py > logs_from_rabbit.log
import pika

# Connecting to RabbitMQ Server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Creating Exchange(X) with Type as Fanout
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Creating A Random Queue With Exclusive as True Means Queue will deleted as soons as Connection Closed
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Binding Exchange to The Queue
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

#Call Back Function
def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# Consume Process
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

# Channel Wil Start Receiving Logs
channel.start_consuming()

