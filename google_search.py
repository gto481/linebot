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
# Perform google search


from chatterbot import ChatBot
import logging
from google import google

#from linebot.models import TextSendMessage, LocationMessage

#from linebot.models import (
#    MessageEvent, TextMessage, TextSendMessage,
#    SourceUser, SourceGroup, SourceRoom,
#    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
#    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
#    CarouselTemplate, CarouselColumn, PostbackEvent,
#    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
#    ImageMessage, ImageSendMessage, VideoMessage, AudioMessage,
#    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea
#)

from linebot.models import (TextSendMessage, TemplateSendMessage, URITemplateAction, CarouselTemplate, CarouselColumn)

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

def search(bot=bot, text=None):
    # Search location
    #response=random.choice(SEARCH_REPLY_MESSAGE)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    columns = []
    i = 0
    message = None
    try:
        g = google.search(text)
        for r in g:
            i += 1
            if ( i > 5):
                break
            if r is not None:
                #print r.google_link
                url = r.google_link
                title=r.name[:40]
                text=r.description[:60]
                #cc = CarouselColumn(text=text, title=title, thumbnail_image_url='/img/google.png', actions=[URITemplateAction(label='Go to website', uri=url)])
                cc = CarouselColumn(text=text, title=title, actions=[URITemplateAction(label='Go to website', uri=url)])
                columns.append(cc)
        carousel_template = CarouselTemplate(columns=columns)
        message = TemplateSendMessage(alt_text='Search result', template=carousel_template)

    except:
        message = TextSendMessage(text=random.choice(BROKEN_MESSAGE))

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

    return message

if __name__ == "__main__":

    msg = search(bot, u"บ้านป๋าเปรม")
    print msg
