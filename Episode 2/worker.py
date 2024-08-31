import time
import pika

# Establishing Connection with RabbitMQ Server
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()

# Creating Queue 
# durable=True ==> Queue and Mesages Stored is not lost , evenif Rabbitmq-server crashes.
channel.queue_declare(queue='task_queue' , durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

# Callback Function
# basic_ack ==> Acknowledges to Queue if the task is processed or not , with delivery tag
def callback(ch , method , properties , body):
    print('[X] Received %r' %body.decode())
    time.sleep(body.count(b'.'))
    print("[X] Task Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

# QOS will tell RabbitMQ not to give more than one message to a worker at a time (Instead Going With The Message Order)
# Don't dispatch a new message to a worker until it has processed and acknowledged the previous one. 
# Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)

# Setting Up Queue and Callback Function
channel.basic_consume(queue='task_queue'  , on_message_callback=callback)

# It will start processing the message at Worker
channel.start_consuming()