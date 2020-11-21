import pika, os, time, logging 
from chatterbot import ChatBot
from bot import TwitterBot, Platform
from config import create_api, create_queue

logger = logging.getLogger()

def recieve_tweets(platform: Platform):
    producer_channel = create_queue('twitter_mentions')
    consumer_channel = create_queue('twitter_mentions')
    def callback(ch, method, properties, body):
        platform.perform_action(msg)

    # set up subscription on the queue
    consumer_channel.basic_consume('twitter_mentions', callback,
    auto_ack=True)
    while True:
        try:
            messages = platform.get_intent()
            for msg in messages:
                logger.info(msg, type(msg))
                producer_channel.basic_publish(exchange='', routing_key='twitter_mentions', body=msg)
            # time.sleep(7200)
            time.sleep(300)
            consumer_channel.start_consuming()
        except Exception as e:
            logger.debug(e)
        finally:
            producer_channel.close()
            consumer_channel.close()

if __name__ == '__main__':
    bot = ChatBot('meenec')
    platform = TwitterBot(bot=bot)
    recieve_tweets(platform)
   

