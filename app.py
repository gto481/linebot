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
    ImageMessage, ImageSendMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea
)

import json
import re
import urllib
from chatterbot import ChatBot
#import geocoder
#from google import google
import pprint
import random
import search_image
import train_bot
import location_bot
import google_search
import ticket_bot
import twitter_bot

TRAIN_REPLY_MESSAGE=["สอนกูแต่เรื่องดีๆนะมึง อีดอก", "มึงคิดกว่ากูฉลาดนักหรอ สอนกูอยู่นั่นแหละ", "ขี้เกียจจำแล้ว"]
LOCATION_REPLY_MESSAGE=["มึงจะหนีเที่ยวที่ไหน อีดอก", "อย่าให้เมียมึงรู้นะว่ามึงหนีเที่ยว", "หาพิกัดผัวมึงหรอ อีดอก"]
SEARCH_REPLY_MESSAGE=["ให้กูหาไมเนี่ย ทำไมไม่หาเอง", "...", "หาเองไม่เป็นหรือ"]

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
msglist = []

commands = (
    (re.compile('^พิกัด[ ]*(.*)'), lambda x: location(x)),
    (re.compile('^[lL]ocation[ ]*(.*)'), lambda x: location(x)),
    (re.compile('^ที่อยู่[ ]*(.*)'), lambda x: location(x)),
    (re.compile('^ค้นหา[ ]*(.*)'), lambda x: googleSearch(x)),
    (re.compile('^หา[ ]*(.*)'), lambda x: googleSearch(x)),
    (re.compile('^[gG]oogle[ ]*(.*)'), lambda x: googleSearch(x)),
    (re.compile('^กูเกิ้ล[ ]*(.*)'), lambda x: googleSearch(x)),
    (re.compile('^กูเกิล[ ]*(.*)'), lambda x: googleSearch(x)),
    (re.compile('^[iI]mage[ ]*(.*)'), lambda x: imageSearch(x)),
    (re.compile('^หารูป[ ]*(.*)'), lambda x: imageSearch(x)),
    (re.compile('^รูป[ ]*(.*)'), lambda x: imageSearch(x)),
    (re.compile('^(ช่วยเหลือ)$'), lambda x: usage()),
    (re.compile('^([hH]elp)$'), lambda x: usage()),
    (re.compile('^[tT]rain[ ]*(.*)$'), lambda x: train(x)),
    (re.compile('^สอน[ ]*(.*)$'), lambda x: train(x)),
    (re.compile('^หาตั๋ว[ ]*(.*)$'), lambda x: ticket(x)),
    (re.compile('^ตั๋ว[ ]*(.*)$'), lambda x: ticket(x)),
    (re.compile('^[tT]icket[ ]*(.*)$'), lambda x: ticket(x)),
    (re.compile('^(มุขตลก)[ ]*(.*)$'), lambda x: joke(x)),
    (re.compile('^(มุข)[ ]*(.*)$'), lambda x: joke(x)),
    (re.compile('^([jJ]oke)[ ]*(.*)$'), lambda x: joke(x)),
)

def usage():
    response="""
1)คุยเล่น
    พิมพ์ห่าอะไรมาก็ได้กูตอบได้
2)Location
    พิกัด <สถานที่>
    location <สถานที่>
    ที่อยู่ <สถานที่>
3)Google search
    ค้นหา <สิ่งที่อยากจะหา>
    หา <สิ่งที่อยากจะหา>
    google <สิ่งที่อยากจะหา>
    กูเกิ้ล <สิ่งที่อยากจะหา>
4)Ticket search
    หาตั๋ว <สถานที่>
    ตั๋ว <สถานที่>
    ticket <สถานที่>
5)Joke
    มุขตลก
    มุข
    joke
6)Help
    แสดงข้อความนี้
7)Train Bot สอนกูแต่เรื่องดีๆนะมึง
    train <ข้อความ>,<ข้อความ>,<ข้อความ>
    """
    #response="1)คุยเล่น\n  พิมพ์ห่าอะไรมาก็ได้กูตอบได้\n2)หาโลเคชั่น\n  พิกัด <สถาที่>\n  location <สถาที่>\n  ที่อยู่ <สถาที่>\n3)Google search\n  ค้นหา <สิ่งที่อยากจะหา>\n  หา <สิ่งที่อยากจะหา>\n  google <สิ่งที่อยากจะหา>\n  กูเกิ้ล <สิ่งที่อยากจะหา>\n4)help\n  แสดงข้อความนี้\n5)Train Bot สอนกูแต่เรื่องดีๆนะมึง\n  train <ข้อความ>,<ข้อความ>,<ข้อความ>"
    message = TextSendMessage(text=response)
    return message

def ticket(text):
    # Fix get data from skyr
    # Call file ticket_bot.py
    message = ticket_bot.getTicket(bot, text)
    return message

def train(text):
    # Training bot with incoming message
    # Call file train_bot.py
    message = train_bot.train(bot, text)
    return message

def location(text):
    # Search location
    # Call file location_bot.py
    message = location_bot.location(bot, text)
    return message

def imageSearch(text):
    # Search Image,
    # beware only 100 query per day
    # call file search_image.py
    #response="ปิดfunctionนี้ก่อนนะ ตังค์เราหมด"
    #return TextSendMessage(text=response)
    message = search_image.getImage(bot, text)
    return message

def googleSearch(text):
    # Search
    # file google_search.py
    template_message = google_search.search(bot, text)
    return template_message

def joke(text):
    # call file twitter_bot.py
    message = twitter_bot.search(bot, text=u"#มุขตลก")
    return message


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
        source = event.source
        print source.user_id
        if event.type == 'message':

            response="พิมพ์เหี้ยอะไรมา กูงง แสรด"
            msg = TextSendMessage(text=response)

            if event.message.type == 'text':

                msg = event.message.text
                # Training bot with incoming message
                #msglist.append(msg)
                #bot.train(msglist)
                flag = False

                for matcher, action in commands:
                    try:
                        m = matcher.search(msg)
                        if (msg == 'userinfo'):
                            flag = True
                            msg = TextSendMessage(text=event.source.user_id)
                            break

                        if m:
                            flag = True
                            text = m.group(1)
                            # line_bot_api.reply_message(
                            #     event.reply_token, action(text)
                            # )
                            msg = action(text)
                            break

                    except:
                        response="พิมพ์เหี้ยอะไรมา กูเจ๊งเลย แสรด"
                        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
                        msg = TextSendMessage(text=response)

                if flag is not True:
                    response = bot.get_response(msg).text.encode('utf-8')
                    #print response
                    #response = event.message.text
                    #print response

                    #line_bot_api.reply_message(
                    #    event.reply_token,
                        #TextSendMessage(result = bot.get_response(event.message.text))
                    #    TextSendMessage(text=response)
                    #)
                    msg = TextSendMessage(text=response)

            elif event.message.type == 'sticker':
                stickerId = random.randint(100,118)
                msg = StickerMessage(package_id=1,sticker_id=stickerId)
                #line_bot_api.reply_message(event.reply_token, StickerMessage(package_id=1,sticker_id=stickerId))

            try:
                line_bot_api.reply_message(event.reply_token, msg)
            except Exception:
                response="พิมพ์เหี้ยอะไรมา กูเจ๊งเลย แสรด"
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))

    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='ทดสอบ'))

    return 'OK'

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
