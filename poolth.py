# -*- coding: utf-8 -*-
import sqlite3
import urllib
import urllib3
import sys
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from arts import arts
from multiprocessing.dummy import Pool as ThreadPool


# фУНКЦИЯ ЧТЕНИЯ ИЗ ФАЙЛОВ
def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


# СКРАППИНГ СТРАНИЦ
def parse_www(uri):
    art = urllib.quote_plus(uri.encode('cp1251'))
    url = url_parse.format(art)
    r = http.request('GET', url)
    data = r.data.decode('cp1251').encode('utf8')
    text_file = open(u"html/{}.html".format(art.encode('utf8')), "w")
    text_file.write(data)
    text_file.close()
    progressbar.update()

# Парстинг HTML соохранение результатов
def parse_html(uri):
    art = urllib.quote_plus(uri.encode('cp1251'))
    text = read_file(u"html/{}.html".format(art))
    soup = BeautifulSoup(text, "html.parser")
    results = soup.find_all('div', {'class': 'eItemProperties_text'})
    price_div = soup.find('div', {'class': 'bSaleColumn'})
    price = None
    if price_div is not None:
        price = price_div.find("span", {"itemprop": "price"})
    description = ''
    price_str = ''
    for res in results:
        description = description + res.text
    if len(description) > 0 and price is not None:
        price_str = price_str + price.text
    re_w = re.compile(' ')
    price_str = re_w.sub('', price_str)
    sql = "INSERT INTO html (art, value, price) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (art, u"{}".format(description), price_str))
        connection.commit()
    except sqlite3.DatabaseError as err:
        print u"Ошибка", err
    else:
        progressbar.set_description(u'Progress parsing ({}) :'.format(art))
        progressbar.update()

# шаблон URL
url_parse = u"http://www.ozon.ru/?context=search&text={}"
# соединение с БД
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
# Выборка уникальных значений из вводного массива
arts_unique = list(set(arts))
# Прогресс бар для индикации работы
progressbar = tqdm(total=len(arts_unique))
# Пулл потоков
pool = ThreadPool(10)
# Менеджер коннектов к сайту
http = urllib3.PoolManager(10)
pool.map(parse_www, arts_unique)
pool.close()
pool.join()

connection.commit()
cursor.close()
connection.close()

