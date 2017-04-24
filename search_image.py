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

import pprint
import random
from apiclient.discovery import build
from linebot.models import (TextSendMessage, ImageSendMessage)
from chatterbot import ChatBot
import logging

DEV_KEY='AIzaSyBnsER5mWY1ajxWFG2PMan9m_acmgxZZJs'
CSE_ID='014879697985822153408:wpjbchhoe3a'
NUM_RESULTS=10
BROKEN_MESSAGE=["กูมึนวะไม่รู้เรื่อง","กูเจ๊งแป๊บบ", "ไม่รู้จักอะ โทษทีที่เรียนมาน้อย"]

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
query=""

def getImage(bot=bot, query=query, num_results=NUM_RESULTS):
    images=[]
    message=None
    try:
        service = build('customsearch', 'v1', developerKey=DEV_KEY)
        res = service.cse().list(
                q = query,
                cx = CSE_ID,
                searchType = 'image',
                num = num_results
        ).execute()
        #pprint.pprint(res)
        for r in res['items']:
            #print r['link']
            #print r['image']['thumbnailLink']
            #dict = {'link' : r['link'], 'thumb' : r['image']['thumbnailLink']}
            image = ImageSendMessage(original_content_url=r['link'], preview_image_url=r['link'])
            images.append(image)

        message = random.choice(images)
    except:
        response=random.choice(BROKEN_MESSAGE)
        message = TextSendMessage(text=response)

    return message

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build('customsearch', 'v1', developerKey=DEV_KEY)
    query = 'rilakkuma'
    res = service.cse().list(
            q = query,
            cx = CSE_ID,
            searchType = 'image',
            num = num_results
    ).execute()
    pprint.pprint(res)

    for r in res['items']:
        print r['link']
        print r['image']['thumbnailLink']

if __name__ == '__main__':
    #main()
    msg = getImage(bot, u'แต้ว')
    print msg
