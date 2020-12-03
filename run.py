import logging
import json, pickle
from chatterbot import ChatBot
from bot import Platform
from config import create_api, create_queue
from utils import create_or_restore_platform_instance

logger = logging.getLogger()


def recieve_tweets(platform: Platform):
    producer_channel = create_queue('twitter_mentions')
    consumer_channel = create_queue('twitter_mentions')


    while True:
        try:
            messages = platform.get_intent()
            for msg in messages:
                logger.info(f' MESSAGE - {msg}')
                producer_channel.basic_publish(exchange='', routing_key='twitter_mentions',
                                               body=json.dumps(msg))
            # consume messages
            for method_frame, properties, body in consumer_channel.consume('twitter_mentions',  inactivity_timeout=200):

                if method_frame is None:
                    break
                msg = json.loads(body)
                # Acknowledge the message
                consumer_channel.basic_ack(method_frame.delivery_tag)
                platform.perform_action(msg)

            # Cancel the consumer and return any pending messages
            requeued_messages = consumer_channel.cancel()
            logger.info(f"Requeued {requeued_messages} messages")
        except Exception as e:
            logger.error(e)



if __name__ == '__main__':
    bot = ChatBot('weenec',
                  logic_adapters=[{
                      'import_path': 'chatterbot.logic.BestMatch',
                      'default_response': "sorry, but i can't seem to find the answer to your question at the moment.",
                      'maximum_similarity_threshold': 0.90
                  }], read_only=True)

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
