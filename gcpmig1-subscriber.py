import time
import os 
from google.cloud import pubsub_v1
credential_path = "C:\\Users\\rsher\\OneDrive\\Desktop\\fog-computing-1989965d0de1.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
project_id = "fog-computing-239019"
subscription_name = "sub-mig1"

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(
    project_id, subscription_name)

def callback(message):
    print('Received message: {}'.format(message))
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)
