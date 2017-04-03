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
import pprint

client = MongoClient('mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6')
db = client.heroku_h80dpwn6
statements = db.statements

pprint.pprint(statements.find_one({"text": "What's your name"}))

#datetime.fromtimestamp(1462629479859/1000.0)

result = db.tickets.insert_one(
	{        
        "userid": "U206d25c2ea6bd87c17655609a1c37cb8",
        "itinerary": [
            {
                "from" : "Thailand",
                "to" : "Vietnum",
                "depart_date": datetime.strptime("2017-04-10", "%Y-%m-%d"),
                "arrive_date": datetime.strptime("2017-04-13", "%Y-%m-%d")
            },
        ]        
    }
)