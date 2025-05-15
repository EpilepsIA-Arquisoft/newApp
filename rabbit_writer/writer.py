import pika

def connect_rabbitmq(host='35.226.31.227', user='isis2503', password='1234'):
    import pika
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                credentials=pika.PlainCredentials(user, password)
            )
        )
        channel = connection.channel()
        return channel
    except pika.exceptions.AMQPConnectionError as e:
        print("Error al conectar con RabbitMQ:", e)
        raise


def publish_message(queue_name, message, channel=None):
    from coder import encrypt_json

    if channel is None:
        channel = connect_rabbitmq()

    channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)
    encrypted_message = encrypt_json(message)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=encrypted_message,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistente
    )
    print(f"Mensaje publicado en la cola '{queue_name}'")



msj={
    "test":"test"
}
connect_rabbitmq()
publish_message('map_requests',msj)