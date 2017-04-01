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

import pprint
from googleapiclient.discovery import build

DEV_KEY='AIzaSyBnsER5mWY1ajxWFG2PMan9m_acmgxZZJs'
CSE_ID='014879697985822153408:wpjbchhoe3a'
NUM_RESULTS=10
list=[]

def getImage(query, num_results=NUM_RESULTS):
    service = build('customsearch', 'v1', developerKey=DEV_KEY)

    res = service.cse().list(
            q = query,
            cx = CSE_ID,
            searchType = 'image',
            num = num_results
    ).execute()
    #pprint.pprint(res)
    for r in res['items']:
        dict = {'link' : r['link'], 'thumb' : r['image']['thumbnailLink']}
        list.append(dict)

    return list

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build('customsearch', 'v1', developerKey=DEV_KEY)
    query = 'rilakkuma'
    res = service.cse().list(
            q = query,
            cx = CSE_ID,
            searchType = 'image',
            num = num_results
    ).execute()
    pprint.pprint(res)

    for r in res['items']:
        print r['link']
        print r['image']['thumbnailLink']

if __name__ == '__main__':
    main()
