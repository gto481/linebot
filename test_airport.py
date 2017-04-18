# -*- coding: utf-8 -*-
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the daddy License.
#
# Perform LTF search

import json
import re
import logging

from pprint import pprint

from chatterbot import ChatBot
from linebot.models import (TextSendMessage)
from pymongo import MongoClient, DESCENDING, ASCENDING
import random

client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
db = client.heroku_h80dpwn6
airports = db.airports

BROKEN_MESSAGE=["กูไม่รู้เรื่องสนามบินไอ้ห่า","กูจน ไม่เคยขึ้นเครื่องบิน", "ไม่รู้จักอะ โทษทีที่เรียนมาน้อย"]

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

def checkAirport(text=None):
    result = airports.find({"$or": [{'City' : text}, {'Country' : text}]})
    return result

def getAirport(bot=bot,text=None):

    result = None
    message = None
    try:
        result = checkAirport(text)

        if result and result.count() > 0:
            #print "fetch new data"
            i = 0
            for r in result:
                #print r['City']
                i += 1
                text = text + "{0}) เมือง {1}, ประเทศ {2}, สนามบิน {3}, code {4}\n".format(i, r['City'], r['Country'], r['Airport'], r['Code'])
            #print text
            message = TextSendMessage(text=text)

    except Exception as e:
        print e
        message = TextSendMessage(text=random.choice(BROKEN_MESSAGE))

    return message

if __name__ == "__main__":

    # msg = getLTF()
    # for r in msg[:5]:
    #    pprint(r)
    msg = getAirport(bot,u'เชียงใหม่'.encode('utf-8'))
    pprint(msg)

    # result = checkDb()
    # if result.count() > 0:
    #     #print "found"
    #     for r in result[:5]:
    #         pprint(r)
