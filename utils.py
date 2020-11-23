"""
    utils.py contains useful utility functions used in bot modules
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


def train_bot(bot: ChatBot, *paths_to_corpus: str):
    '''
        train_bot trains a chatterbot.ChatBot object passed as an argument
        :param 
        bot: ChatBot
        paths_to_corpus: [str]
    '''
    trainer = ChatterBotCorpusTrainer(bot)
    print(f'*** starting training bot ***')
    trainer.train(*paths_to_corpus)
    print(f'*** finished training bot ***')


def create_or_restore_bot_instance():
    '''
        create new ChatBot instance if stored instance could not be restored
    '''
    pass