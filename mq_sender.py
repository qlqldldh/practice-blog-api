from MQClient import MQClient
import json

if __name__ == "__main__":
    mq_client = MQClient()

    # message = "hello i'm sender by mq client"
    message = {"intro": "Hello", "words": "worlds"}  # dict
    msg = json.dumps(message)
    mq_client.publish(message=msg)
