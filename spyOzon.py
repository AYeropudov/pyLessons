# -*- coding: utf-8 -*-
import sqlite3
import urllib
import urllib3
from bs4 import BeautifulSoup
from lxml import html
from arts import arts

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


#url_parse = "http://wstat.ozon.ru/tracker/v0?events=searchQuery&pageViewId=15000351102440.09154516580776506&g=http%3A%2F%2Fwww.ozon.ru%2F&r=&v29=main_page&ns=ozon&v2={}&v103=search_keyword_client&rc=4"
url_parse = u"http://www.ozon.ru/?context=search&text={}"

# conection = sqlite3.connect('db.sqlite')
for art in arts:
    art = urllib.quote_plus(art.encode('cp1251'))
    url = url_parse.format(art)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    data = r.data.decode('cp1251').encode('utf8')
    text_file = open(u"html/{}.html".format(art), "w")
    text_file.write(data)
    text_file.close()
#text = read_file(u"html/{}.html".format(art))
# sql = "INSERT INTO html (html, art) VALUES (?, ?)"
# try:
#     cursor.execute(sql, (data, art))
# except sqlite3.DatabaseError as err:
#     print u"Ошибка", err
# else:
#     print u"Запрос успешен"
#     conection.commit()
# cursor.close()
# conection.close()
#soup = BeautifulSoup(text, "html.parser")
#res = soup.find_all('div', {'class': 'eItemProperties_text'})
#for e in res:
#    print e.text
#print(res)

