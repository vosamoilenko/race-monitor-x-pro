import pika
import json
import os
import logging
from dotenv import load_dotenv
from firebase.Firebase import Firebase

# Load environment and set up logging
load_dotenv()
BASE_PATH = os.environ.get("BASE_PATH")
logging.basicConfig(filename=f"{BASE_PATH}/obd-rally-golf/logs/consumer.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Firebase setup
fb = Firebase()
FAKE_FIREBASE = os.environ.get("FAKE_FIREBASE")


# RabbitMQ connection setup
credentials = pika.PlainCredentials('portal', 'none')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

settings = fb.get_settings()

def send_to_firebase(queue_name, data):
    logging.info(f"Sending data to Firebase from {queue_name}: {data}")
    if FAKE_FIREBASE != 'true':
        fb.push(queue_name, data)
        logging.info("Data sent to Firebase")

def callback(ch, method, properties, body, queue_name):
    logging.info(f"Received message from {queue_name}: {body}")
    data = json.loads(body)
    send_to_firebase(settings['currentRacerId'], data)

def setup_consumer(queue_name):
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, queue_name),
        auto_ack=True
    )

# Setup consumers for multiple queues
queues = ['gps', 'obd']
for queue in queues:
    setup_consumer(queue)

logging.info('Waiting for messages from all sources. To exit press CTRL+C')
channel.start_consuming()
