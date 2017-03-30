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

import geocoder
import sys
import re
import json

#g = geocoder.google("ซันทาวเวอร์")
#print g.latlng

#commands = (
#    (re.compile('ต่ำแหน่ง[ ]*(.*)'), lambda x: location(x.group(1))),
#    (re.compile('location[ ]*(.*)'), lambda x: location(x.group(1))),
#    (re.compile('ที่อยู่[ ]*(.*)'), lambda x: location(x.group(1))),
#)
commands = (
    (re.compile('ต่ำแหน่ง[ ]*(.*)'), lambda x: location(x)),
    (re.compile('location[ ]*(.*)'), lambda x: location(x)),
    (re.compile('ที่อยู่[ ]*(.*)'), lambda x: location(x))
)

def location(text):
    g = geocoder.google(text)
    #print g.latlng
    return g


if __name__ == "__main__":
	msg = "location ซันทาวเวอร์"
#	location('ซันทาวเวอร์')
	flag = False
	
	for matcher, action in commands:		
		m = matcher.search(msg)
		
		if m:
			flag = True
			g = action(m.group(1))
			print g.lat
			print g.lng
			#print g.json
			#print g.wkt
			#print g.osm
			#print g.address						
	
	if flag is not True:
		print "not found."

