# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging
import sys
import random
import json

from linebot.models import TextSendMessage

# Uncomment the following line to enable verbose logging
# logging.basicConfig(level=logging.INFO)

TRAIN_REPLY_MESSAGE=["สอนกูแต่เรื่องดีๆนะมึง อีดอก", "มึงคิดกว่ากูฉลาดนักหรอ สอนกูอยู่นั่นแหละ", "ขี้เกียจจำแล้ว"]
BROKEN_MESSAGE=["กูมึนวะไม่รู้เรื่อง","กูเจ๊งแป๊บบ"]

# Create a new ChatBot instance
bot = ChatBot('LineBot',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    database='heroku_h80dpwn6',
    database_uri='mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6'
)

def train(bot=bot, x=None):
    # Training bot with incoming message
    msglist = x.split(",")
    print msglist
    bot.set_trainer(ListTrainer)
    bot.train(msglist)
    response=random.choice(TRAIN_REPLY_MESSAGE)
    message = TextSendMessage(text=response)
    return message

if __name__ == "__main__":

    print('Input is file conversation...')
    conversation_file = sys.argv[1]
    conversations = json.loads(open(conversation_file).read())
    print ("[-] Start training bot")
    bot.set_trainer(ListTrainer)
    bot.train(conversations)
    print ("[-] Train success")
