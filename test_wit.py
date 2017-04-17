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

def parse(bot=bot,text=None):
    message=None
    try:
        print "Start parsing"
        print text
        dateMessage = re.compile(ur'.*(วันนี้|พรุ่งนี้|มรืนนี้|เสาร์ทิตย์|สุดสัปดาห์|วันหยุด|สัปดาห์หน้า|สัปดาห์ถัดไป|วันก่อน|เดือนหน้า).*'.encode('utf-8'), re.UNICODE)
        dateFound = dateMessage.search(text)
        dateStr=None
        if dateFound:
            print "Parsing date"
            dateStr=dateFound.group(1)
            text=text.replace(dateStr,'')
        else:
            print "found no date"

        matcher = re.compile(ur'.*(ฉัน|กู|มึง|นาย|เธอ|เรา|คุณ|ผม)*[ ]*(ต้องการ|อยากได้|อยากให้|ทำให้|ช่วย|ช่วยเหลือ|จอง|จองตั๋ว|ออกตั๋ว|ค้นหา|หา|ดู)[ ]*(ตั๋ว|ตั๋วเครื่องบิน|เครื่องบิน)[ ]*(จาก)*(กรุงเทพ|กทม)*(ไป)*(เชียงใหม่)'.encode('utf-8'), re.UNICODE)
        found = matcher.search(text)
        if found:
            print "found String"
            reply="Time is {}, Subject is {}, verb is {}, object1 is {}, conjunction1 is {}, object2 is {}, conjunction2 is {}, object3 is {}".format(dateStr,found.group(1),found.group(2),
                found.group(3),found.group(4),found.group(5),found.group(6),found.group(7))
            message = TextSendMessage(text=reply)
        else:
            print "found nothing"
            message = TextSendMessage(text='What!!!')
        print message
    except Exception,e:
        print str(e)
    return message

if __name__ == "__main__":

    str = u"อยากได้ตั๋วกทมไปเชียงใหม่".encode('utf-8')
    msg = parse(bot,str)
    pprint(msg)