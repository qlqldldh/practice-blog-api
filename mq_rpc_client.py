import json
import ssl
import uuid

from pika import BasicProperties, BlockingConnection, PlainCredentials, SSLOptions, ConnectionParameters

context = ssl._create_unverified_context()


class RpcClient:
    request_queue = "request_queue"
    result_queue = "result_queue"
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
        self.channel.queue_declare(queue=self.result_queue, durable=True)

        self.channel.basic_consume(queue=self.result_queue, on_message_callback=self.on_response)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        corr_id = str(self.corr_id)
        if corr_id == props.correlation_id:
            print("correlation id in response : ", self.corr_id)
            print("body: ", body)
            self.response = body

    def call(self, req):
        self.response = None
        self.corr_id = int(uuid.uuid4())
        print("send correlation id: ", self.corr_id)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.request_queue,
            properties=BasicProperties(
                reply_to=self.result_queue,
                correlation_id=str(self.corr_id)
            ),
            body=json.dumps(req),
        )

        while self.response is None:
            self.connection.process_data_events()

        return json.loads(self.response)


if __name__ == "__main__":
    rpc_client = RpcClient()
    # send to rpc_server in this project
    # num_msg = input("put in a number: ")
    #
    # print("put number: ", num_msg)

    # send to rpc_server in lunar
    request = {"first_value": "animal", "second_value": "crack"}

    resp = rpc_client.call(request)
    print("type: ", type(resp))
    print(resp)
