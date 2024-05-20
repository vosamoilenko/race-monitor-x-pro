# mq/PikaClientProducer.py
import pika

class PikaClientProducer:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        credentials = pika.PlainCredentials('portal', 'none')
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def send(self, data):
        self.channel.basic_publish(exchange='',
                          routing_key=self.queue_name,
                          body=str(data))

    def close():
        self.connection.close()
