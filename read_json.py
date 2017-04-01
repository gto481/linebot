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

import json
from pprint import pprint

with open('ticketout.json') as data_file:
    data = json.load(data_file)
pprint(data)

i = 0
list_results = list(data['results'])
list_records = list(list(list_results))
for r in list_records:
    i += 1
    if (i > 5):
        break
    #print r
    #m = eval(r)
    text="""
        {0}
        {1} @ {2}
        {3} @ {4}
        {5}
        {6} @ {7}
        {8} @ {9}
        Price {10} {11}
        """.format(r['Inbound_Airline'],r['Inbound_Departure_Airport'],r['Inbound_Departure_DT'],r['Inbound_Arrival_Airport'],r['Inbound_Arrival_DT'],
        r['Outbound_Airline'],r['Outbound_Arrival_Airport'],r['Outbound_Arrival_DT'],r['Outbound_Departure_Airport'],r['Outbound_Departure_DT'],r['Total_Price'],r['Currency'])
    print text
