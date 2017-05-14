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

import requests
import json
import re
import logging

from pprint import pprint
from operator import itemgetter
from bs4 import BeautifulSoup
from signal import signal, SIGPIPE, SIG_DFL

from chatterbot import ChatBot
from linebot.models import (TextMessage)
from pymongo import MongoClient, DESCENDING, ASCENDING
from datetime import datetime, date, timedelta
import random

signal(SIGPIPE,SIG_DFL)

#client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
#db = client.heroku_h80dpwn6

BROKEN_MESSAGE=["เอิ่ม กูทำอาหารไม่เป็น","กูแดกอย่างเดียว ไม่ทำอาหาร", "ไม่รู้จักอะ โทษทีที่เรียนมาน้อย"]
APP_ID='98e72d17'
APP_KEY='0774d98769245bad049bcd6a2fc8aa46'

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


def getRecipe(bot=bot,text=None,resultFrom=0,resultTo=3,calories=None,health=None):

    result = None

    print "Search edamam"

    #https://api.edamam.com/search?q={0}&app_id={1}&app_key={2}&from=0&to=3&calories=gte%20591,%20lte%20722&health=alcohol-free"

    #calories="gte%20591,%20lte%20722"
    try:
        base_url = "https://api.edamam.com/search?q={0}&app_id={1}&app_key={2}&from={3}&to={4}".format(text,APP_ID,APP_KEY,resultFrom,resultTo)

        if (calories) :
            base_url = base_url + "&calories={}".format(calories)
        if (health) :
            base_url = base_url + "health={}".format(health)

        r = requests.get(base_url)
        r.headers['content-type']
        r.encoding = 'utf-8'
        today = datetime.today()

        jsonObj = r.json()
        #print jsonObj['hits'][0]

        #pprint(jsonObj)

        message = ""
        print "Get result"
        for recipe in jsonObj['hits']:
            #print recipe['recipe']['label']
            message = message + ", name : " + recipe['recipe']['label'] + ", ingredients : "

            for ingredients in recipe['recipe']['ingredientLines']:
                #print ingredients
                message = message + ingredients
            message = message + "\n"

        result = TextMessage(text=message)
        print result

    except:
        result = TextMessage(text=random.choice(BROKEN_MESSAGE))

    return result

# def getLTFMessage(bot=bot):
#     message = None
#     try:
#         x = getLTF()
#         if x is not None and x.count() > 0:
#             text = "แม่งกากและยังโง่อีก\n\n"
#             i = 0
#             for r in x:
#                 i += 1
#                 text = text + "{0}) {1}, {2}, 5year {3}, 3year {4}, NAV {5}\n".format(i, r['mutual_fund'], r['institution'], r['perf_5year'], r['perf_3year'], r['NAV'])
#             message = TextMessage(text=text)
#     except:
#         message = TextMessage(text=random.choice(BROKEN_MESSAGE))

#     return message

if __name__ == "__main__":

    # msg = getLTF()
    # for r in msg[:5]:
    #    pprint(r)
    msg = getRecipe("chicken")
    print(msg)

    # result = checkDb()
    # if result.count() > 0:
    #     #print "found"
    #     for r in result[:5]:
    #         pprint(r)
