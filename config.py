import tweepy
import logging
import os
import dotenv 

logger = logging.getLogger()

dotenv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
else:
    raise ValueError(f'could not find config file at {os.path.dirname(dotenv_file)}')

def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def create_queue(name):
    import pika
    logging.basicConfig()

    # Parse CLOUDAMQP_URL (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL')
    params = pika.URLParameters(f"{url}/?connection_attempts=3&heartbeat=0&retry_delay=60")
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.queue_declare(queue=name) # Declare a queue
    return channel
