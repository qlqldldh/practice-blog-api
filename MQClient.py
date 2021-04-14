import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials, SSLOptions
import ssl

context = ssl._create_unverified_context()


class MQClient:
    HOST = "localhost"
    PORT = 5672
    credential = PlainCredentials("user", "pass")
    request_queue = "req_queue"
    result_queue = "res_queue"

    def __init__(self):
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=self.HOST,
                port=self.PORT,
                virtual_host="/",
                credentials=self.credential,
                ssl_options=SSLOptions(context),
            )
        )
        self.channel = self.connection.channel()

    def publish(self, message):
        self.channel.queue_declare(queue=self.request_queue, durable=True)

        self.channel.basic_publish(exchange="", routing_key=self.request_queue, body=message)
        print(f"publish message: {message}")
        self.connection.close()

    def subscribe(self):
        self.channel.queue_declare(queue=self.result_queue, durable=True)

        self.channel.basic_consume(queue=self.result_queue, auto_ack=True, on_message_callback=self.callback)
        print("\nMQ Client ... Start Consuming ...\n")
        self.channel.start_consuming()

    def callback(self, ch, method, props, body):
        print("method: ", method)
        print(body)
        print("type: ", type(body))

        msg = json.loads(body)
        print(msg)
        print("type: ", type(msg))
