"""
    train.py trains bot conservations using  an INEC FAQ data source
    :url  https://www.inecnigeria.org/voter-education/faqs/
"""

import sys
from chatterbot import ChatBot
from utils import train_bot
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("corpus path was not specified")
    bot = ChatBot('weenec')
    train_bot(bot,sys.argv[1])
