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
# Perform location check


from chatterbot import ChatBot
import logging
import random
import geocoder

from linebot.models import TextMessage, LocationMessage

# Uncomment the following line to enable verbose logging
# logging.basicConfig(level=logging.INFO)

BROKEN_MESSAGE=["กูมึนวะไม่รู้เรื่อง","กูเจ๊งแป๊บบ", "ไม่รู้จักอะ โทษทีที่เรียนมาน้อย"]

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

def location(bot=bot, text=None):
    # Search location
    #response=random.choice(LOCATION_REPLY_MESSAGE)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    #print "start get location " + text
    print "get location"
    message = None
    try:
        g = geocoder.google(text)
        #print g.latlng
        title=text[:100]
        address=g.address[:100]
        #print title
        #print address
        message = LocationMessage(title=title, address=address, latitude=g.lat, longitude=g.lng)
    except:
        response=random.choice(BROKEN_MESSAGE)
        message = TextMessage(text=response)

    return message

if __name__ == "__main__":

    msg = location(bot, "บ้านป๋าเปรม")
    print msg
