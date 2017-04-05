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

from pymongo import MongoClient
from pprint import pprint
from datetime import datetime, date, timedelta

client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
db = client.heroku_h80dpwn6
tickets = db.tickets
xxx = db.xxx
#statements = db.statements
#pprint(statements.find_one({"text": "What's your name"}))

#datetime.fromtimestamp(1462629479859/1000.0)

# result = db.tickets.insert_one(
# 	{
#         "userId": "U206d25c2ea6bd87c17655609a1c37cb8",
#         "createdAt" : datetime.now(),
#         "itinerary": [
#             {
#                 "from" : "Thailand",
#                 "to" : "Vietnum",
#                 "departDate": datetime.strptime("2017-04-10", "%Y-%m-%d"),
#                 "arriveDate": datetime.strptime("2017-04-13", "%Y-%m-%d")
#             },
#         ],
#         "isDeleted" : 0,
#         "lastModified" : None,
#     }
# )

lasthours = datetime.today() - timedelta(hours = 1)
#yesterday = datetime.combine(yesterday, datetime.time.min)
#print yesterday
#tickets = db.tickets.find_one({'userid' : 'U206d25c2ea6bd87c17655609a1c37cb8'})
ticket = tickets.find_one({'userid' : 'U206d25c2ea6bd87c17655609a1c37cb8', 'createdAt' : {'$gte' : lasthours}})
if ticket:
    pprint(ticket)
else:
    print "empty result"
    #result = tickets.delete_many({'userid' : 'U206d25c2ea6bd87c17655609a1c37cb8', 'created_at' : {'$lt' : lasthours}})
    result = tickets.update_many({'userId' : 'U206d25c2ea6bd87c17655609a1c37cb8', 'createdAt' : {'$lt' : lasthours}},
        {"$set" : { "isDeleted" : "1" }, "$currentDate": {"lastModified": True} })
    print result
