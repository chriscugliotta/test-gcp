"""
Testing Google Pub/Sub.

References:
    - Quickstart:
      https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library

    - Publisher Client:
      https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.publisher.client.Client

    - Subscriber Client:
      https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.client.Client
"""
from concurrent.futures import TimeoutError
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.cloud.pubsub_v1.subscriber.message import Message



class Config:
    """Contains input variables and config."""
    def __init__(self):
        self.project_id: str = 'curious-entropy-199817'
        self.topic_id: str = 'test-topic-1'
        self.sub_id: str = 'test-sub-1'
        self.creds_file: Path = Path(__file__).parents[1] / 'infra' / 'test_service_account' / 'key.json'
        self.creds: Credentials = Credentials.from_service_account_file(self.creds_file)


def publish_messages(config: Config, publisher: PublisherClient):
    """Publishes N messages to a topic."""
    for i in range(3):
        future = publisher.publish(
            topic=publisher.topic_path(config.project_id, config.topic_id),
            data=f'Hello world {i}'.encode('utf-8'),
        )
        result = future.result()
        print(f'Published message {i}, result = {result}.')


def receive_messages(config: Config, subscriber: SubscriberClient):
    """Receives (and acknowledges) all pending messages in a topic."""
    print(f'Listening for messages on:  {config.sub_id}.')
    streaming_pull_future = subscriber.subscribe(
        subscription=subscriber.subscription_path(config.project_id, config.sub_id),
        callback=on_received,
    )
    with subscriber:
        try:
            streaming_pull_future.result(timeout=5)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


def on_received(message: Message):
    """Async callback function, i.e. fired once per received message."""
    print(f'Received message, data = {message.data}.')
    message.ack()



if __name__ == '__main__':
    """Main method."""
    print('Begin.')
    config = Config()
    publisher = PublisherClient(credentials=config.creds)
    subscriber = SubscriberClient(credentials=config.creds)
    publish_messages(config, publisher)
    receive_messages(config, subscriber)
    print('Done.')
