import pika
from .decoder import decrypt_json

def connect_rabbitmq(host='10.128.0.20', user='isis2503', password='1234'):
    """
    Establece conexión con RabbitMQ y retorna un canal.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            credentials=pika.PlainCredentials(user, password)
        )
    )
    channel = connection.channel()
    return channel

def consume_messages(queue_name, channel=connect_rabbitmq(), wait_forever=True, max_messages=1):
    """
    Declara la cola (la crea si no existe) y consume mensajes.

    - wait_forever = True: se queda esperando infinitamente.
    - wait_forever = False: solo procesa hasta max_messages.
    """
    # Crear la cola si no existe
    channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)

    consumed = 0

    def callback(ch, method, properties, body):
        nonlocal consumed

        # Descifrar mensaje
        entrada = decrypt_json(body)
        print(f"Mensaje recibido: {entrada}")

        # Procesar mensaje si quieres (opcional)
        # post_message(entrada)

        # Confirmar recepción
        ch.basic_ack(delivery_tag=method.delivery_tag)

        # Si no es espera infinita, parar al llegar al límite
        consumed += 1
        if not wait_forever and consumed >= max_messages:
            ch.stop_consuming()

    # Iniciar consumidor
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(f"Escuchando mensajes en '{queue_name}'...")
    channel.start_consuming()