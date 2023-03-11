# amqps://nwftptjj:tI4EvJbv-9OHk6k1U2jvCHyQ3XsL4Yc0@puffin.rmq2.cloudamqp.com/nwftptjj

import pika
import json
import logging
logging.basicConfig(level=logging.INFO)
from models import Product
from models import db
from app import app

params = pika.URLParameters('amqps://nwftptjj:tI4EvJbv-9OHk6k1U2jvCHyQ3XsL4Yc0@puffin.rmq2.cloudamqp.com/nwftptjj')

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')

with pika.BlockingConnection(params) as connection:
    with connection.channel() as channel:

        channel.queue_declare(queue='main')
        def callback(ch, method, properties, body):
            with app.app_context():  # Create a Flask application context
                logging.info("Received: In message ")
                data = json.loads(body)
                logging.info(data)

                if properties.content_type == 'product_created':
                    product = Product(id=data['id'], title=data['title'], image=data['image'])

                    db.session.add(product)
                    db.session.commit()
                    logging.info("product created")
                elif properties.content_type == 'product_updated':
                    product = db.session.query(Product).get(data['id'])
                    product.title = data['title']
                    product.image = data['image']
                    db.session.commit()
                    logging.info("product updated")

                elif properties.content_type == 'product_deleted':
                    product = db.session.query(Product).get(data)
                    db.session.delete(product)
                    db.session.commit()
                    logging.info("product deleted")


        channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)


        logging.info("Start Consuming")
        channel.start_consuming()

