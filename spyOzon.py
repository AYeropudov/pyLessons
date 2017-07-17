# -*- coding: utf-8 -*-
import sqlite3
import urllib
import urllib3

import sys
from bs4 import BeautifulSoup
from lxml import html
import re
from tqdm import tqdm
from arts import arts

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


#url_parse = "http://wstat.ozon.ru/tracker/v0?events=searchQuery&pageViewId=15000351102440.09154516580776506&g=http%3A%2F%2Fwww.ozon.ru%2F&r=&v29=main_page&ns=ozon&v2={}&v103=search_keyword_client&rc=4"
url_parse = u"http://www.ozon.ru/?context=search&text={}"
conection = sqlite3.connect('db.sqlite')
cursor = conection.cursor()
arts_uniq = list(set(arts))
pbar = tqdm(total=len(arts_uniq))


def parse_www(arts):
    for art in arts:
        art = urllib.quote_plus(art.encode('cp1251'))
        url = url_parse.format(art)
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        data = r.data.decode('cp1251').encode('utf8')
        text_file = open(u"html/{}.html".format(art.encode('utf8')), "w")
        text_file.write(data)
        text_file.close()


def parse_html(arts):
    i = 0
    for art in arts:
        art = urllib.quote_plus(art.encode('cp1251'))
        text = read_file(u"html/{}.html".format(art))
        soup = BeautifulSoup(text, "html.parser")
        results = soup.find_all('div', {'class': 'eItemProperties_text'})
        price_div = soup.find('div', {'class': 'bSaleColumn'})
        price = None
        if price_div is not None:
            price = price_div.find("span", {"itemprop": "price"})
        str = ''
        pricse_str = ''
        for res in results:
            str = str + res.text
        if len(str) > 0 and price is not None:
            pricse_str = pricse_str + price.text
        re_w = re.compile(' ')
        pricse_str = re_w.sub('', pricse_str)
        sql = "INSERT INTO html (art, value, price) VALUES (?, ?, ?)"
        try:

            cursor.execute(sql, (art, u"{}".format(str), pricse_str))
            conection.commit()
        except sqlite3.DatabaseError as err:
            print u"Ошибка", err
        else:
            i += 1
            # progress(i, len(arts), art)
            pbar.set_description(u'Progress parsing ({}) :'.format(art))
            pbar.update(i)
    conection.commit()
    cursor.close()
    conection.close()


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    print '{} {} ...{} {}\r'.format(bar, percents, '%', suffix)
#soup = BeautifulSoup(text, "html.parser")
#res = soup.find_all('div', {'class': 'eItemProperties_text'})
#for e in res:
#    print e.text
#print(res)
#parse_www(arts=arts_uniq)
parse_html(arts=arts_uniq)

