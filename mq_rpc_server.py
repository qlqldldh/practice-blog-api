import ssl

from pika import BlockingConnection, BasicProperties, PlainCredentials, SSLOptions, ConnectionParameters

context = ssl._create_unverified_context()


class RpcServer:
    request_queue = "request_queue"
    HOST = "localhost"
    PORT = 5672
    credential = PlainCredentials("user", "pass")

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

        self.channel.queue_declare(queue=self.request_queue, durable=True)

    def consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.request_queue, on_message_callback=self.on_request)

        print("Start Consuming ...")
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        n = int(body)

        print("received number: ", n)
        resp_n = n*n

        print("received correlation id: ", props.correlation_id)

        ch.basic_publish(exchange="", routing_key=props.reply_to, properties=BasicProperties(correlation_id=props.correlation_id), body=str(resp_n))
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    rpc_server = RpcServer()

    rpc_server.consuming()
