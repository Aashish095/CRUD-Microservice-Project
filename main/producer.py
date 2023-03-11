# amqps://nwftptjj:tI4EvJbv-9OHk6k1U2jvCHyQ3XsL4Yc0@puffin.rmq2.cloudamqp.com/nwftptjj

import pika
import json

params = pika.URLParameters('amqps://nwftptjj:tI4EvJbv-9OHk6k1U2jvCHyQ3XsL4Yc0@puffin.rmq2.cloudamqp.com/nwftptjj')

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method,body):
    print("publish",body)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body),properties=properties)


