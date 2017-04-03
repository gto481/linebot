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
import json
from datetime import datetime

from pymongo import MongoClient
from linebot.models import TextSendMessage

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

# Create a Mongo client
client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
db = client.heroku_h80dpwn6

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

def getTicket(bot=bot, input=None):

    # Fix get data from skyr

    # 1) Search database check that user already ask for it or not


    message = None
    try:
        with open('ticketout.json') as data_file:
            data = json.load(data_file)
        #pprint(data)
        i = 0
        columns = []
        list_results = list(data['results'])
        list_records = list(list(list_results))
        for r in list_records:
            i += 1
            if (i > 5):
                break
            #title=r['Agency_Name']
            #print title
            description="""{0}{1}
Out {2}
Dep. {3}@{4}
In {5}
Dep. {6}@{7}""".format(r['Total_Price'],r['Currency'],
                r['Outbound_Airline'],
                #r['Outbound_Arrival_Airport'],r['Outbound_Arrival_DT'],
                r['Outbound_Departure_Airport'],r['Outbound_Departure_DT'],
                r['Inbound_Airline'],
                r['Inbound_Departure_Airport'],r['Inbound_Departure_DT'],
                #r['Inbound_Arrival_Airport'],r['Inbound_Arrival_DT'],
                )
            description = description[:100]
            url = r['Reservation_Link']
            cc = CarouselColumn(text=description, actions=[URITemplateAction(label='Book', uri=url)])
            columns.append(cc)

        carousel_template = CarouselTemplate(columns=columns)
        message = TemplateSendMessage(alt_text='Search result', template=carousel_template)
    except:
        response=random.choice(BROKEN_MESSAGE)
        message = TextSendMessage(text=response)

    return message

if __name__ == "__main__":

    msg = getTicket(bot, u"vietnum")
    print msg
