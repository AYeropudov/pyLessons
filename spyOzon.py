# -*- coding: utf-8 -*-
import sqlite3
import urllib
import urllib3
from bs4 import BeautifulSoup
from lxml import html


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


#url_parse = "http://wstat.ozon.ru/tracker/v0?events=searchQuery&pageViewId=15000351102440.09154516580776506&g=http%3A%2F%2Fwww.ozon.ru%2F&r=&v29=main_page&ns=ozon&v2={}&v103=search_keyword_client&rc=4"
url_parse = u"http://www.ozon.ru/?context=search&text={}"

conection = sqlite3.connect('db.sqlite')
cursor = conection.cursor()
url = url_parse.format(urllib.quote_plus(u'ЩЯ-500'.encode('cp1251')))
http = urllib3.PoolManager()
r = http.request('GET', url)
data = r.data.decode('cp1251').encode('utf8')
text_file = open("Output.html", "w")
text_file.write(data)
text = read_file("Output.html")
soup = BeautifulSoup(text, "html.parser")
res = soup.find_all('div', {'class': 'eItemProperties_text'})
for e in res:
    print e.text
# print(res)

