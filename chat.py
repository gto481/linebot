#!/usr/bin/python
#-*-coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
import sys

BOT_NAME = "LineBot"
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


if len(sys.argv) < 2:
  sys.exit(0)

message = sys.argv[1]
result = bot.get_response(message)
print ("%s" % result)