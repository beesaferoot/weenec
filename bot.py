import typing 
import logging
from chatterbot import ChatBot
from abc import ABC, abstractmethod
import tweepy

logging.basicConfig(level=logging.INFO)



class Platform(ABC):
    '''
        Base Platform Scope for bot
    '''
    def __init__(self, name='', config: typing.Dict[str, object]=None, bot: ChatBot=None):
        self.name = name
        self.config = config
        self.bot = bot

    @abstractmethod
    def get_intent(self):
        raise NotImplementedError

    @abstractmethod
    def perform_action(self, message: str):
        raise NotImplementedError


class TwitterBot(Platform):
    '''
        twitter platform scope for bot
    '''

    def __init__(self, api: tweepy.API=None, since_id=1, **kwargs):
        super().__init__(name='twitter', **kwargs)
        self.api = api
        self.since_id = since_id
    
    def get_intent(self):
        return self.get_mentions()

    def perform_action(self, message):
        self.send_message(message)

    def get_mentions(self):
        messages = []
        for tweet in tweepy.Cursor(self.api.mentions_timeline, since_id=self.since_id).items(50):
            self.since_id = max(tweet.id, self.since_id)
            if tweet.in_reply_to_status_id is not None:
                continue

            if len(tweet.text):
                messages.append((tweet.text.lower(), tweet.id, tweet.user.screen_name))
        return messages

    def send_message(self, msg):
        message, tweet_id, tweet_user_name = msg
        response = f"@{tweet_user_name} {self.bot.get_response(message)}"
        print(response, tweet_id)
        self.api.update_status(status=response,
            in_reply_to_status_id=tweet_id)


