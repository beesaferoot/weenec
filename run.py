import logging
import json
import threading
from chatterbot import ChatBot
from bot import TwitterBot
from config import create_api, create_queue
from utils import create_or_restore_platform_instance, update_platform_state

logger = logging.getLogger()


def receive_tweets(platform: TwitterBot):
    producer_channel = create_queue('twitter_mentions')
    consumer_channel = create_queue('twitter_mentions')

    while True:
        try:
            messages = platform.get_intent()
            logger.info(f' MESSAGES - {messages}')
            for msg in messages:
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
        finally:
            update_platform_state(since_id=platform.since_id)


if __name__ == '__main__':
    bot = ChatBot('weenec',
                  logic_adapters=[{
                      'import_path': 'chatterbot.logic.BestMatch',
                      'default_response': "sorry, but i can't seem to find the answer to your question at the moment."
                                          "for more info visit https://www.inecnigeria.org/voter-education/faqs/.",
                      'threshold': 0.90
                  }], read_only=True,
                  preprocessors=['chatterbot.preprocessors.clean_whitespace'],
                  silence_performance_warning=True
                  )

    platform = create_or_restore_platform_instance()
    platform.bot = bot
    platform.api = create_api()
    receive_tweets(platform)

