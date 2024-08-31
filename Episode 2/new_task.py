import sys
import pika 

# Establishing Connection with RabbitMQ Server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()

# Creating Queue
channel.queue_declare(queue='task_queue' , durable=True)

# Input Taken From Console (More . (dots) means More Time-Consuming-Tasks)
# Example ==> Order Of Processing Time : ==>  hello... < hi........... < bye...................
message=' '.join(sys.argv[1:]) or "Hello World!"

# Publishing Message and Marking Message as Persistent(Durable)
channel.basic_publish(exchange='' , routing_key='task_queue' , body=message  ,
                    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

print('[X] Sent %r' %message)

# Closing Connection
connection.close()