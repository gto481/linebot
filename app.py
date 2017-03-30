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

from __future__ import unicode_literals

import os
import sys
import time

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea
)

import json
import re
# import nltk.corpus
# import nltk.tokenize.punkt
# import nltk.stem.snowball
# from nltk.corpus import wordnet
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import geocoder
import pprint
from random import randint

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

# Create a new chat bot named Charlie
bot = ChatBot('LineBot',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
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
bot.set_trainer(ListTrainer)
msglist = []

commands = (
    (re.compile('พิกัด[ ]*(.*)'), lambda x: location(x)),
    (re.compile('location[ ]*(.*)'), lambda x: location(x)),
    (re.compile('ที่อยู่[ ]*(.*)'), lambda x: location(x))
)

def location(text):
    g = geocoder.google(text)
    #print g.latlng
    return g

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)    

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        pprint.pprint(event)
        if event.type == 'message':

            if event.message.type == 'text':

                msg = event.message.text            
                # Training bot with incoming message
                #msglist.append(msg)
                #bot.train(msglist)                
                flag = False

                for matcher, action in commands:
                    m = matcher.search(msg)
                    if m:
                        flag = True
                        title = m.group(1)
                        g = action(title)
                        line_bot_api.reply_message(
                            event.reply_token,
                            LocationMessage(title=title, address=g.address, latitude=g.lat, longitude=g.lng)
                        )
                        break
                
                if flag is not True:
                    response = bot.get_response(msg).text.encode('utf-8')
                    #print response            
                    #response = event.message.text 
                    #print response            

                    line_bot_api.reply_message(
                        event.reply_token,
                        #TextSendMessage(result = bot.get_response(event.message.text))
                        TextSendMessage(text=response)
                    )

            elif event.message.type == 'sticker':                
                stickerId = randint(1,21)
                line_bot_api.reply_message(event.reply_token, StickerMessage(package_id=1,sticker_id=stickerId))

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
