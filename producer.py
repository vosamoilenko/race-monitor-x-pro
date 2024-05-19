import pika

credentials = pika.PlainCredentials('portal', 'none')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='data_queue')

def send_to_queue(data):
    channel.basic_publish(exchange='',
                          routing_key='data_queue',
                          body=str(data))
    print(" [x] Sent data")

# Example usage
send_to_queue({'gps': '51.5033640,-0.1276250', 'obd': 'speed 30'})
connection.close()
