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

from pymongo import MongoClient, ASCENDING
from pprint import pprint
from datetime import datetime, date, timedelta
import json
import time

current_milli_time = lambda: int(round(time.time() * 1000))

# Mongo connection
client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
db = client.heroku_h80dpwn6
conversation = db.conversation

def insert(app=None,userid=None,timestamp=None,inmsg=None,outmsg=None):
    print "App {}, userid {}, timestamp {}, inmsg {}, outmsg {}".format(app,userid,timestamp,inmsg,outmsg)
    if userid and app:
        try:
            msg = {
                "timestamp" : current_milli_time(),
                "application" : app,
                "receive": {
                    "userId": userid,
                    "timestamp" : timestamp,
                    "message" : dict(inmsg)
                },
                "reply": {
                    "userId": userid,
                    "timestamp" : current_milli_time(),
                    "message" :  dict(outmsg)
                }
            }
            print dict(msg)
            print dict(inmsg)
            print dict(outmsg)
            #result = conversation.insert_one(dict(msg))
        except Exception as e:
            print e
    return None

if __name__ == "__main__":
    insert("line","U206d25c2ea6bd87c17655609a1c37cb8",1493198938675,{"id": "5994924103238", "text": "\u0e42\u0e22\u0e48\u0e46", "type": "text"},{"text": "\u0e2b\u0e48\u0e32\u0e25\u0e32\u0e01", "type": "text"})