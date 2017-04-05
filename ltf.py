# -*- coding: utf-8 -*-
import requests
import json
import re
from pprint import pprint
from operator import itemgetter
from bs4 import BeautifulSoup
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

r = requests.get('http://www.thaifundstoday.com/en/funds?Fund+Type=ltf&tab=long&unit=p&sortcol=11')
r.encoding = 'utf-8'

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
for row in rows:
    cols=row.find_all('td')
    num_field=1
#	cols=[{(num_field):x.text.strip()} for x in cols]
    for col in cols:
        value="field"+str(num_field)
        y=re.sub('[%]','',col.text)
        value_str = str(y).replace('\nD','').replace('\nT','').strip().rstrip().lstrip()
        #print "value_str = {}".format(value_str)
        if re.match("^[+-]*\d+?\.\d+?$", value_str):
            value1 = float(value_str)
        else:
	       value1 = value_str
        #new_cols.append({(value):y.strip()})

        #print "value = {}".format(value1)
        if (num_field==1):
            new_cols.append({(value):value1})
        else:
            new_cols[(list_no)][(value)]=value1

        num_field=num_field+1

    #print "new_cols = {}".format(new_cols)
    list_no=list_no+1

#data = json.dumps({'results': new_cols})
x = sorted(new_cols, key=itemgetter('field12'), reverse=True)
for r in x:
    pprint(r)
