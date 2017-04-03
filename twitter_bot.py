# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

import tweepy
from linebot.models import (TextSendMessage)
from chatterbot import ChatBot
import logging
import random

CONSUMER_KEY = 'CBtungI0UsL4zi0UaWvpyAh5E'
CONSUMER_SECRET = 'IWkykwZNTAGYniempFlyT2e1DhA951HCImwKJN7dz1VFixZyJi'
ACCESS_KEY = '758328481193136128-BufWUoupPHlZ9Omcoc3C0CJWKwzebVC'
ACCESS_SECRET = 'lvjzChypQRhv9pZXelWApn7ElkIul17MnjzmbDqo9DGxa'
NUM_RESULTS=5
BROKEN_MESSAGE=["กูเป็นคนไม่ตลกวะ","กูหมดมุขแหละ", "ขอโทษนะ กูเป็นคนซีเรียส"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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

def search(bot=bot, text=u"#มุขตลก"):

	message = None
	try:		
		search_result = api.search(text, rpp=NUM_RESULTS)
		texts = []
		for i in search_result:
			texts.append(i.text)

		text = random.choice(texts)
		message = TextSendMessage(text=text)

	except:
		message = TextSendMessage(text=random.choice(BROKEN_MESSAGE))
	
	return message

if __name__ == '__main__':
    #main()
    msg = search(bot, u'#แต้ว')
    print msg
