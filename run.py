import pika, os, time, logging 
import json
from chatterbot import ChatBot
from bot import TwitterBot, Platform
from config import create_api, create_queue
from utils import train_bot, create_or_restore_bot_instance

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
                # print(msg, type(msg))
                producer_channel.basic_publish(exchange='', routing_key='twitter_mentions', 
                    body=json.dumps(msg))
            # time.sleep(7200)
            time.sleep(500)
            consumer_channel.start_consuming()
        except Exception as e:
            logger.debug(e)
            print(e)        
            # producer_channel.close()
            # consumer_channel.close()


if __name__ == '__main__':
    bot = create_or_restore_bot_instance()  
    train_bot(bot, 'data/faq_corpus/')
    platform = TwitterBot(bot=bot, api=create_api())
    recieve_tweets(platform)
   

