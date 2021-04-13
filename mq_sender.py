from MQClient import MQClient

if __name__ == "__main__":
    mq_client = MQClient()

    message = "hello i'm sender by mq client"
    mq_client.publish(message=message)
