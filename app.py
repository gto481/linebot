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
import urllib
# import nltk.corpus
# import nltk.tokenize.punkt
# import nltk.stem.snowball
# from nltk.corpus import wordnet
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import geocoder
from google import google, images
import pprint
import random

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
bot.set_trainer(ListTrainer)
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
    4)Help
        แสดงข้อความนี้
    5)Train Bot สอนกูแต่เรื่องดีๆนะมึง
        train <ข้อความ>,<ข้อความ>,<ข้อความ>
    """
    #response="1)คุยเล่น\n  พิมพ์ห่าอะไรมาก็ได้กูตอบได้\n2)หาโลเคชั่น\n  พิกัด <สถาที่>\n  location <สถาที่>\n  ที่อยู่ <สถาที่>\n3)Google search\n  ค้นหา <สิ่งที่อยากจะหา>\n  หา <สิ่งที่อยากจะหา>\n  google <สิ่งที่อยากจะหา>\n  กูเกิ้ล <สิ่งที่อยากจะหา>\n4)help\n  แสดงข้อความนี้\n5)Train Bot สอนกูแต่เรื่องดีๆนะมึง\n  train <ข้อความ>,<ข้อความ>,<ข้อความ>"
    message = TextSendMessage(text=response)
    return message

def ticket(x):
    response="อีหอยใช้กูจังเลยนะ กูขี้เกียจหา"
    message = TextSendMessage(text=response)
    return message

def train(x):
    # Training bot with incoming message
    msglist = x.split(",")
    print msglist
    bot.train(msglist)
    response=random.choice(TRAIN_REPLY_MESSAGE)
    message = TextSendMessage(text=response)
    return message

def location(text):
    # Search location
    #response=random.choice(LOCATION_REPLY_MESSAGE)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    g = geocoder.google(text)
    #print g.latlng
    title=text[:100]
    address=g.address[:100]
    if g is not None:
        message = LocationMessage(title=title, address=address, latitude=g.lat, longitude=g.lng)
    else:
        response="ไม่รู้จักอะ โทษทีที่เรียนมาน้อย"
        message = TextSendMessage(text=response)

    return message

def imageSearch(text):

    print "doing image search"
    options = images.ImageOptions()
    g = google.search_images(text, options)
    print "get image"
    images = []
    i = 0
    #try:
    for r in g:
        i += 1
        if ( i > 5):
            break
        if r is not None:
            print r.link
            url = r.link
            thumb = r.thumb
            image = ImageSendMessage(original_content_url=url, preview_image_url=thumb)
            images.append(image)

    template_message = random.choice(images)
    return template_message

def googleSearch(text):
    # Search location
    #response=random.choice(SEARCH_REPLY_MESSAGE)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    g = google.search(text)
    columns = []
    i = 0
    #try:
    for r in g:
        i += 1
        if ( i > 5):
            break
        if r is not None:
            print r.google_link
            url = r.google_link
            title=r.name[:40]
            text=r.description[:60]
            cc = CarouselColumn(text=text, title=title, actions=[URITemplateAction(label='Go to website', uri=url)])
            columns.append(cc)
            print columns
    #    actions = [URITemplateAction(label='More Detail', uri=r.link)]
    #     carousel_column = CarouselColumn(text=r.description.encode('utf-8'), title=r.name.encode('utf-8'), actions=actions)
    #     columns.append(carousel_column)

    carousel_template = CarouselTemplate(columns=columns)
    #carousel_template = CarouselTemplate(columns=columns)
    #template_message = TemplateSendMessage(alt_text='Buttons alt text', template=carousel_template)
    template_message = TemplateSendMessage(alt_text='Search result', template=carousel_template)
    # carousel_template = CarouselTemplate(columns=[
    #         CarouselColumn(text='hoge1', title='fuga1', actions=[
    #             URITemplateAction(
    #                 label='Go to line.me', uri='https://line.me'),
    #             PostbackTemplateAction(label='ping', data='ping')
    #         ]),
    #         CarouselColumn(text='hoge2', title='fuga2', actions=[
    #             PostbackTemplateAction(
    #                 label='ping with text', data='ping',
    #                 text='ping'),
    #             MessageTemplateAction(label='Translate Rice', text='米')
    #         ]),
    #     ])
    # template_message = TemplateSendMessage(alt_text='Buttons alt text', template=carousel_template)
    #except Exception:
    #    response="ค้นหาไม่ได้วะ โทษที กูโง่"
    #    template_message = TextSendMessage(text=response)
    return template_message

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
                        if m:
                            flag = True
                            text = m.group(1)
                            # line_bot_api.reply_message(
                            #     event.reply_token, action(text)
                            # )
                            msg = action(text)
                            break
                    except Exception:
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
