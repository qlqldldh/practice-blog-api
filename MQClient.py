from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class MQClient:
    HOST = "localhost"
    queue = "req_queue"
    credential = PlainCredentials("dean", "dean")

    def __init__(self):
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=self.HOST, port=5672, virtual_host="/", credentials=self.credential
            )
        )
        self.channel = self.connection.channel()
        self.connection.process_data_events()

    def publish(self, message):
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(exchange="", routing_key=self.queue, body=message)
        print(f"publish message: {message}")
        self.connection.close()

    def subscribe(self):
        self.channel.queue_declare(queue="req_queue")

        self.channel.basic_consume(queue="req_queue", auto_ack=True, on_message_callback=self.callback)
        print("\nMQ Client ... Start Consuming ...\n")
        self.channel.start_consuming()

    def callback(self, ch, method, props, body):
        print("method: ", method)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        print(f"received message: {body}")
        resp_message = "received well done ~ friend~!"
        ch.basic_publish(exchange="", routing_key="req_queue", body=resp_message)
