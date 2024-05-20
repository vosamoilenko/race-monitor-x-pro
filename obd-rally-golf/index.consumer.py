from waveshare.waveshare import Waveshare
import json

waveshare = Waveshare()

# data = {
#     "a": {"integerValue": 123}
# }

waveshare.sendToFirebase(data)


# import pika

# def setup_consumer(queue_name):
#     # Declare the queue
#     channel.queue_declare(queue=queue_name)
    
#     # Setup a consumer callback
#     def callback(ch, method, properties, body):
#         print(" [x] Received from {}: {}".format(queue_name, body))
    
#     # Start consuming from the queue
#     channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# # Establish connection
# credentials = pika.PlainCredentials('portal', 'none')
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost', credentials=credentials))
# channel = connection.channel()

# # Setup consumers for multiple queues
# queues = ['gps', 'obd']  # Example of multiple queues
# for queue in queues:
#     setup_consumer(queue)

# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
