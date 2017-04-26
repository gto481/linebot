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
# Perform LTF search

import requests
import json
import re
import logging

from pprint import pprint
from operator import itemgetter
from bs4 import BeautifulSoup
from signal import signal, SIGPIPE, SIG_DFL

from chatterbot import ChatBot
from linebot.models import (TextMessage)
from pymongo import MongoClient, DESCENDING, ASCENDING
from datetime import datetime, date, timedelta
import random

signal(SIGPIPE,SIG_DFL)

client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
db = client.heroku_h80dpwn6
ltf = db.ltf

BROKEN_MESSAGE=["กูไม่รู้เรื่อง LTF","กูจน ไม่เล่น LTF", "ไม่รู้จักอะ โทษทีที่เรียนมาน้อย"]

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

def checkDb():
    last10hours = datetime.today() - timedelta(hours = 10)
    result = ltf.find({'created_at' : {'$gte' : last10hours}}).sort("perf_5year", DESCENDING)
    execute = ltf.delete_many({'created_at' : {'$lt' : last10hours}})
    return result

def getLTF():

    result = None
    result = checkDb()

    if result.count() < 1:
        #print "fetch new data"
        r = requests.get('http://www.thaifundstoday.com/en/funds?Fund+Type=ltf&tab=long&unit=p&sortcol=11')
        r.encoding = 'utf-8'
        today = datetime.today()

        final_col=[]
        new_cols=[]
        list_no=0
        soup = BeautifulSoup(r.content, 'lxml')
        #soup = BeautifulSoup(open("/tmp/out4.txt"), 'lxml')

        table = soup.find("table", id="fundsTable")

        #headers = [td.get_text() for td in table.find_all("tr")[0].find_all("td")]
        #print(headers)
        table_body=table.find('tbody')
        rows = table_body.find_all('tr')
        i = 0
        for row in rows:
            cols=row.find_all('td')
            i += 1
            num_field=1
        #	cols=[{(num_field):x.text.strip()} for x in cols]
            for col in cols:

                name = None
                if num_field == 12:
                    name = 'perf_5year'
                elif num_field == 2:
                    name = 'mutual_fund'
                elif num_field == 3:
                    name = 'institution'
                elif num_field == 4:
                    name = 'NAV'
                elif num_field == 11:
                    name = 'perf_3year'

                #name="field"+str(num_field)
                v=re.sub('[%]','',col.text)
                value_str = str(v).replace('\nD','').replace('\nT','').strip().rstrip().lstrip()
                #print "value_str = {}".format(value_str)
                if re.match("^[+-]*\d+?\.\d+?$", value_str):
                    value = float(value_str)
                else:
        	       value = value_str
                #new_cols.append({(value):y.strip()})

                #print "value = {}".format(value1)
                if (num_field==1):
                    name = 'item'
                    new_cols.append({(name): i })
                else:
                    if name is not None:
                        new_cols[(list_no)][(name)]=value

                num_field=num_field+1
                new_cols[(list_no)]['created_at']=today

            #print "new_cols = {}".format(new_cols)
            list_no=list_no+1

        #data = json.dumps({'results': new_cols})
        result = sorted(new_cols, key=itemgetter('perf_5year'), reverse=True)
        try:
            ltf.insert_many(result)
            ltf.create_index([("perf_5year", DESCENDING)])
        except:
            pass
        #for r in x[:5]:
        #    pprint(r)
    #else:
        #pprint(result)
        # for r in result:
        #     pprint(r)
        #sorted(result, key=itemgetter('perf_5year'), reverse=True)
        #pprint(result)
        #print "found record {}".format(result.count())

    return result[:5]

def getLTFMessage(bot=bot):
    message = None
    try:
        x = getLTF()
        if x is not None and x.count() > 0:
            text = "แม่งกากและยังโง่อีก\n\n"
            i = 0
            for r in x:
                i += 1
                text = text + "{0}) {1}, {2}, 5year {3}, 3year {4}, NAV {5}\n".format(i, r['mutual_fund'], r['institution'], r['perf_5year'], r['perf_3year'], r['NAV'])
            message = TextMessage(text=text)
    except:
        message = TextMessage(text=random.choice(BROKEN_MESSAGE))

    return message

if __name__ == "__main__":

    # msg = getLTF()
    # for r in msg[:5]:
    #    pprint(r)
    msg = getLTFMessage(bot)
    pprint(msg)

    # result = checkDb()
    # if result.count() > 0:
    #     #print "found"
    #     for r in result[:5]:
    #         pprint(r)
