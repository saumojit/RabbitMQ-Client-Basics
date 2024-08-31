import pika
import sys

#Connection
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

#Channel
channel=connection.channel()

#Exchange(X) -- Direct
channel.exchange_declare(exchange='direct_logs' , exchange_type='direct')

# Creating A Random Queue With Exclusive as True Means Queue will deleted as soons as Connection Closed
result=channel.queue_declare(queue='',exclusive=True)
queue_name=result.method.queue


#Reading inputs : classifying which kind of routing key we want to accept
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

#Binding
#Exchange -> Queue
for severity in severities:
    channel.queue_bind(queue=queue_name , exchange='direct_logs' ,routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

#Call Back Function #body comes from publish in emit
def callback(ch, method, properties, body):
    print(" [x] %r: %r" % (method.routing_key, body))

#Readying Channel to Consume
channel.basic_consume(queue=queue_name , on_message_callback=callback ,auto_ack=True)

# Channel Wil Start Receiving Logs
channel.start_consuming()




# Console
# python receive_logs_direct.py info warning error
# python receive_logs_direct.py warning > logs_from_rabbit.log