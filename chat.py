#!/usr/bin/python
#-*-coding: utf-8 -*-
from chatterbot import ChatBot
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
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    database='heroku_h80dpwn6',
    database_uri='mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6'
)

input_raw = "เฮโหล"
input = input_raw.decode("utf-8")

result = bot.get_response(input).text.encode('utf-8')
f1=open('./output', 'w+')
print >> f1, result