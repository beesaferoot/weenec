import pika, os, time, logging 
import json, pickle
from chatterbot import ChatBot
from bot import Platform
from config import create_api, create_queue
from utils import train_bot, create_or_restore_platform_instance

logger = logging.getLogger()

def recieve_tweets(platform: Platform):
    producer_channel = create_queue('twitter_mentions')
    consumer_channel = create_queue('twitter_mentions')
    
    def callback(ch, method, properties, body):
        platform.perform_action(json.loads(body))

    # set up subscription on the queue
    consumer_channel.basic_consume('twitter_mentions', callback,
    auto_ack=True)
    
    while True:
        try:
            messages = platform.get_intent()
            print("messages - ", messages)
            for msg in messages:
                logger.debug(msg, type(msg))
                producer_channel.basic_publish(exchange='', routing_key='twitter_mentions', 
                    body=json.dumps(msg))
            time.sleep(500)
            consumer_channel.start_consuming()
        except Exception as e:
            logger.debug(e)
                         
    producer_channel.close()
    consumer_channel.close()

if __name__ == '__main__':
    bot = ChatBot('weenec')  
    train_bot(bot, 'data/faq_corpus/')
    platform = create_or_restore_platform_instance()
    platform.bot = bot
    platform.api = create_api()
    try:
        recieve_tweets(platform)
    finally:
        with open("platform_state.pickle", "wb") as state:
            cur_state = {}
            cur_state["since_id"] = platform.since_id
            pickle.dump(cur_state, state)

