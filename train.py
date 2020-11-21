"""
    train.py trains bot conservations using  as  INEC FAQ data source
    :url  https://www.inecnigeria.org/voter-education/faqs/
"""


if __name__ == '__main__':
    from chatterbot import ChatBot
    from utils import train_bot
    
    bot = ChatBot('weenec')
    train_bot(bot=bot)