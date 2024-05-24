import pika
import json
from collections import defaultdict
from waveshare.waveshare import Waveshare
import subprocess
import logging
import redis
import time

# Set up basic logging
logging.basicConfig(filename="logs.txt",level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to Redis
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def get_access_token():
    logging.info("Obtaining access token using gcloud")
    try:
        result = subprocess.check_output(['gcloud', 'auth', 'print-access-token'])
        access_token = result.decode('utf-8').strip()
        logging.info("Access token obtained")
        return access_token
    except subprocess.CalledProcessError as e:
        logging.error("Failed to obtain access token: %s", e.output)
        return None

access_token = get_access_token()

# Initialize Waveshare object
waveshare = Waveshare()

# Establish connection
credentials = pika.PlainCredentials('portal', 'none')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

# Data storage for queues
data_storage = defaultdict(dict)

def adjust_to_firebase_format(data):
    firebase_data = {}
    for key, value in data.items():
        if isinstance(value, float):
            firebase_data[key] = {'doubleValue': value}
        elif isinstance(value, int):
            firebase_data[key] = {'integerValue': value}
        else:
            firebase_data[key] = {'stringValue': str(value)}
    return firebase_data

def process_and_send_to_firebase():
    if 'gps' in data_storage and 'obd' in data_storage:
        # Combine the data
        combined_data = data_storage['gps'].copy()
        combined_data.update(data_storage['obd'])
        logging.info("Processing and sending data to Firebase: %s", combined_data)
        formatted_data = adjust_to_firebase_format(combined_data)
        
        r.set('pause_gps', 'true')
        time.sleep(1)

        waveshare.sendToFirebase(formatted_data, access_token)

        time.sleep(2)
        r.set('pause_gps', 'false')

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
