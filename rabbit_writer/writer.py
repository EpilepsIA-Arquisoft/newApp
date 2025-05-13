import pika

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

def publish_message(queue_name, message, channel=connect_rabbitmq()):
    from .coder import encrypt_json

    """
    Declara la cola (la crea si no existe) y envía el mensaje cifrado.
    """
    # Crear la cola si no existe
    channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)

    # Cifrar el mensaje
    encrypted_message = encrypt_json(message)

    # Publicar en la cola
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=encrypted_message,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistente
    )
    print(f"Mensaje publicado en la cola '{queue_name}'")
