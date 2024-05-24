import pika
import json
import os
from collections import defaultdict
import subprocess
import logging
import time
from dotenv import load_dotenv
from firebase.Firebase import Firebase

logging.basicConfig(filename="/home/pi/Developer/py/obd-rally-golf/logs/consumer.log",level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up basic logging
fb = Firebase()

load_dotenv()

FAKE_FIREBASE = os.environ.get("FAKE_FIREBASE")

# Establish connection
credentials = pika.PlainCredentials('portal', 'none')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

# Data storage for queues
data_storage = defaultdict(dict)

def process_and_send_to_firebase():
    if 'gps' in data_storage and 'obd' in data_storage:
        # Combine the data
        combined_data = data_storage['gps'].copy()
        combined_data.update(data_storage['obd'])
        logging.info("Processing and sending data to Firebase: %s", combined_data)

        if FAKE_FIREBASE != 'true':
            fb.push('vova',combined_data)
            logging.info("Data sent to Firebase")

        data_storage.clear()

def callback(ch, method, properties, body, queue_name):
    print("QUEUE {} {}".format(queue_name, body))
    data_storage[queue_name] = json.loads(body)
    process_and_send_to_firebase()

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
