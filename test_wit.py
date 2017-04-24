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
from wit import Wit
import thai_icu
import re

from chatterbot import ChatBot
from linebot.models import (TextSendMessage)
from pprint import pprint
import dateparser
import test_airport

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

access_token='RSM2P46QTNCZWHPHCUA55UAJNI7LIP73'

# def send(request, response):
#     print('Sending to user...', response['text'])
# def my_action(request):
#     print('Received from user...', request['text'])

# actions = {
#     'send': send,
#     'my_action': my_action,
# }

# client = Wit(access_token=access_token, actions=actions)

# str=u'จองตั๋ววันนี้จากกรุงเทพไปเชียงใหม่'



# icu_list=thai_icu.wrap(str)
# icu_str=" ".join(icu_list)
# print icu_str


#resp = client.message(icu_str)
#print('Yay, got Wit.ai response: ' + str(resp))

keyword = (
    (re.compile('^check|list[ ]*(.*)', re.IGNORECASE), lambda x: checkTicket(x)),
    (re.compile('^book|buy[ ]*(.*)', re.IGNORECASE), lambda x: bookTicket(x)),
    (re.compile('^boarding[ ]*pass|pass[ ]*(.*)', re.IGNORECASE), lambda x: boardingPass(x)),
    (re.compile('^itinerary|ticket[ ]*information[ ]*(.*)', re.IGNORECASE), lambda x: itinerary(x)),
)

def parse(bot=bot,text=None):
    message=None
    try:
        print text
        dateMessage = re.compile(ur'.*(วันนี้|พรุ่งนี้|มรืนนี้|เสาร์ทิตย์|สุดสัปดาห์|วันหยุด|สัปดาห์หน้า|สัปดาห์ถัดไป|วันก่อน|เดือนหน้า).*'.encode('utf-8'), re.UNICODE)
        dateFound = dateMessage.search(text)
        dateStr=None
        if dateFound:
            dateStr=dateFound.group(1)
            text=text.replace(dateStr,'')
            date=dateparser.parse(dateStr)
        else:
            print "found no date"

        matcher1 = re.compile(ur'.*(ฉัน|กู|มึง|นาย|เธอ|เรา|คุณ|ผม)*[ ]*(ต้องการ|อยากได้|อยากให้|ทำให้|ช่วย|ช่วยเหลือ|จอง|จองตั๋ว|ออกตั๋ว|ค้นหา|หา|ดู)[ ]*(ตั๋ว|ตั๋วเครื่องบิน|เครื่องบิน)[ ]*(จาก)*(กรุงเทพ|กทม)*(ไป)*(เชียงใหม่)'.encode('utf-8'), re.UNICODE)
        matcher2 = re.compile(ur'.*(ฉัน|กู|มึง|นาย|เธอ|เรา|คุณ|ผม)*[ ]*(อยากไป|ไป)*[ ]*([^ ]+)'.encode('utf-8'), re.UNICODE)
        found1 = matcher1.search(text)
        if found1:
            print "found1 String"
            reply="Time is {}, Subject is {}, verb is {}, object1 is {}, conjunction1 is {}, object2 is {}, conjunction2 is {}, object3 is {}".format(date,found1.group(1),found1.group(2),
                found1.group(3),found1.group(4),found1.group(5),found1.group(6),found1.group(7))
            message = TextMessage(text=reply)
        elif found2:
            print "found2 String"
            if found2.group(3):
                result = test_airport.checkOneAirport(found2.group(3))

            reply="Time is {}, verb is {}, object1 is {}".format(date,found2.group(1),found2.group(2),found2.group(3))
            if result:
                msg = " เมือง {1}, ประเทศ {2}, สนามบิน {3}\n".format(r['City'].encode('utf-8'), r['Country'].encode('utf-8'), r['Airport'].encode('utf-8'))
                reply = reply + msg

            message = TextMessage(text=reply)
        else:
            print "found nothing"
            message = TextMessage(text='What!!!')


        # for matcher, action in keyword:

        print message
    except Exception,e:
        print str(e)
    return message

if __name__ == "__main__":

    str = u"อยากได้ตั๋วกทมไปเชียงใหม่".encode('utf-8')
    msg = parse(bot,str)
    pprint(msg)