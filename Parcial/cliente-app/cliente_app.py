import os
import time
import requests
import pika
from flask import Flask, jsonify

app = Flask(__name__)

SERVICE_ID = os.environ.get('SERVICE_ID', 'unknown')
API_REGISTRO_URL = "http://registro-app:5000/registro"
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://admin:admin@rabbitmq:5672')

def registrar_servicio():
    headers = {"X-Service-ID": SERVICE_ID}
    try:
        response = requests.post(API_REGISTRO_URL, headers=headers)
        print(f"[{SERVICE_ID}] Registro: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"[{SERVICE_ID}] Error: {e}")
        return {"error": str(e)}

def publicar_mensaje(mensaje):
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue='logs')
        channel.basic_publish(exchange='', routing_key='logs', body=mensaje)
        print(f"[{SERVICE_ID}] Mensaje publicado: {mensaje}")
        connection.close()
    except Exception as e:
        print(f"[{SERVICE_ID}] Error publicando mensaje: {e}")

@app.route('/')
def index():
    result = registrar_servicio()
    mensaje = f"Servicio {SERVICE_ID} registrado con éxito"
    publicar_mensaje(mensaje)
    return jsonify({
        "service": SERVICE_ID,
        "registered": result
    })

if __name__ == "__main__":
    # Registrar periódicamente en segundo plano
    import threading
    def periodic_register():
        while True:
            registrar_servicio()
            time.sleep(10)  # Cada 10 segundos
    
    threading.Thread(target=periodic_register, daemon=True).start()
    
    # Iniciar servidor web
    app.run(host="0.0.0.0", port=5000)