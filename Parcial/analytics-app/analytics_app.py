import pika
import os

RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://admin:admin@rabbitmq:5672')

def callback(ch, method, properties, body):
    print(f"Peticcion recibido: {body.decode()}")

def main():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue='logs')
    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)
    print("Esperando Peticcion...")
    channel.start_consuming()

if __name__ == "__main__":
    main()