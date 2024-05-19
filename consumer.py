import pika

credentials = pika.PlainCredentials('portal', 'none')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='gps')

def callback(ch, method, properties, body):
    print(" [x] Received {}".format(body))

channel.basic_consume(queue='gps', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
