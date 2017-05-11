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
#conversation = db.conversation

doctors = db.doctors



#airports = db.airports

#statements = db.statements
#pprint(statements.find_one({"text": "What's your name"}))

#datetime.fromtimestamp(1462629479859/1000.0)

# Insert
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

# Query
# lasthours = datetime.today() - timedelta(hours = 1)
# #yesterday = datetime.combine(yesterday, datetime.time.min)
# #print yesterday
# #tickets = db.tickets.find_one({'userid' : 'U206d25c2ea6bd87c17655609a1c37cb8'})
# ticket = tickets.find_one({'userid' : 'U206d25c2ea6bd87c17655609a1c37cb8', 'createdAt' : {'$gte' : lasthours}})
# if ticket:
#     pprint(ticket)
# else:
#     print "empty result"
#     #result = tickets.delete_many({'userid' : 'U206d25c2ea6bd87c17655609a1c37cb8', 'created_at' : {'$lt' : lasthours}})
#     result = tickets.update_many({'userId' : 'U206d25c2ea6bd87c17655609a1c37cb8', 'createdAt' : {'$lt' : lasthours}},
#         {"$set" : { "isDeleted" : "1" }, "$currentDate": {"lastModified": True} })
#     print result

# airport = airports.find_one({ 'City' : "Bangkok"})
# pprint(airport)


# Insert

# with open('json/eng_airport.json') as json_data:
#     airport_obj = json.load(json_data)
#     for i in airport_obj:
#         results = airports.insert(airport_obj[i])

        #for k, v in i.items():
        #    print k, v

#airports.create_index([("Country", ASCENDING)])
#airports.create_index([("City", ASCENDING)])


# result = conversation.insert_one(
#   {
#         "timestamp" : current_milli_time(),
#         "application" : "line",
#         "receive":
#             {
#                 "userId": "U206d25c2ea6bd87c17655609a1c37cb8",
#                 "timestamp" : current_milli_time(),
#                 "message" : {"id": "5994896050706", "text": "\u0e42\u0e22\u0e48", "type": "text"}
#             },
#         "reply":
#             {
#                 "userId": "U206d25c2ea6bd87c17655609a1c37cb8",
#                 "timestamp" : current_milli_time(),
#                 "message" :  {"text": "\u0e2b\u0e48\u0e32\u0e25\u0e32\u0e01", "type": "text"}
#             }

#     }
# )

# result = doctors.insert_one(
#     {
#         "created_date" : current_milli_time(),
#         "updated_date" : current_milli_time(),
#         "name"  : "John Smith",
#         "hospital" : "Chicago Hospital",
#         "occupy" : "Dentist"
#     }
# )

# schedules = db.doctor_schedules

# schedules.insert_one(
#     {
#         "name" : "John Smith",
#         "calendar" : [
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 12:00", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 13:30", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 14:00", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 1,
#                 "patient" : "Antonio Aflonso"
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 14:30", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 15:00", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 1,
#                 "patient" : "John Appleseed"
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 15:30", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 16:00", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-09 16:30", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#         ]
#     }
# )

doctos = db.doctors
doctor_schedules = db.doctor_schedules
# doctor_schedules.insert_one(
#     {
#         "name" : "John Smith",
#         "calendar" : [
#             {
#                 "working_hour" : datetime.strptime("2017-05-08 15:30", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#             {
#                 "working_hour" : datetime.strptime("2017-05-08 16:00", "%Y-%m-%d %H:%M"),
#                 "period" : 30,
#                 "book" : 0,
#             },
#         ]
#     }
# )

# schedules.create_index([("working_hour", ASCENDING)])
# schedules.create_index([("book", ASCENDING)])
# schedules.create_index([("name", ASCENDING)])

tomorrow = datetime.strptime("2017-05-09", "%Y-%m-%d")
#print(tomorrow)
doctor = doctos.find_one({'occupy' : 'Dentist'})
#print(doctor['name'])
#bookings = schedules.find({'name' : doctor['name'] , 'working_hour' : {'$gte' : tomorrow}, 'book' : 0} )
#schedules = doctor_schedules.find({'calendar' : { 'working_hour' : {'$gte' : tomorrow}}} )
#schedules = doctor_schedules.find({'calendar.working_hour' : {'$gte' : tomorrow}, 'calendar.book' : 0} )

#schedules = doctor_schedules.find({'name' : doctor['name'], 'calendar.working_hour' : {'$gte' : tomorrow}})
schedules = doctor_schedules.find({'calendar' : { '$elemMatch' : {'book' : 0}}})

for schedule in schedules:
    pprint(schedule)