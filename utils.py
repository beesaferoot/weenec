"""
    utils.py contains useful utility functions used in bot modules
"""
import pickle, os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from bot import Platform, TwitterBot


def train_bot(bot: ChatBot, *paths_to_corpus: str):
    """
        train_bot trains a chatterbot.ChatBot object passed as an argument
        :param
        bot: ChatBot
        paths_to_corpus: [str]
    """
    trainer = ChatterBotCorpusTrainer(bot)
    print(f'*** starting training bot ***')
    trainer.train(*paths_to_corpus)
    print(f'*** finished training bot ***')


def create_or_restore_platform_instance() -> Platform:
    """
        create new ChatBot instance if stored instance could not be restored
        :returns Platform
    """
    try:
        if os.path.exists("platform_state.pickle"):
            with open("platform_state.pickle", "rb") as state:
                bot_state = pickle.load(state)
            return TwitterBot(**bot_state)
        else:
            return TwitterBot()
    except:
        return TwitterBot()


def update_platform_state(**kwargs):
    with open("platform_state.pickle", "wb") as state:
        pickle.dump(kwargs, state)

