#!/usr/bin/env python
import pika , sys , os

def main():
    # Establishing Connection with RabbitMQ Hosted on Localhost
    connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel=connection.channel()

    # Creating Queue # Queue Will Be Created Once Even Though Executing Queue Declaration Multiple Times
    # Best Practise : Same Queue Should Be Declared In Two Programs ( Send / Receive.py )
    channel.queue_declare(queue='hello')


    # Callback which gets triggered once it recvs a message from queue
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # Next , Telling this callback function will recv messages from 'hello' queue
    channel.basic_consume(queue='hello',auto_ack=True,on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C ')
    channel.start_consuming()


if(__name__=="__main__"):
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)