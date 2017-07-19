# -*- coding: utf-8 -*-
import sqlite3
import urllib
import urllib3
import sys
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from arts import arts
from concurrent import futures
import collections

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
    text_file = open(u"/home/alex/spider/html/{}.html".format(art.encode('utf8')), "w")
    text_file.write(data)
    text_file.close()
    return


# Парстинг HTML соохранение результатов
def parse_html(uri):
    art = urllib.quote_plus(uri.encode('cp1251'))
    text = read_file(u"/home/alex/spider/html/{}.html".format(art))
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
    sqls.append((art, u"{}".format(description), price_str))


# очередь
def task_queue(task, iterator, pool):
    counter = collections.Counter()
    with pool as executor:
        to_do_map = {}
        for uri in sorted(iterator):
            future = executor.submit(task, uri)
            to_do_map[future] = uri
        done_iter = futures.as_completed(to_do_map)
        done_iter = tqdm(done_iter, total=len(iterator))
        for future in done_iter:
            counter['status'] += 1
    return counter

# шаблон URL
url_parse = u"http://www.ozon.ru/?context=search&text={}"
# соединение с БД
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
sqls = []
# Выборка уникальных значений из вводного массива
arts_unique = list(set(arts))
# Прогресс бар для индикации работы
# Пулл потоков
#executor = futures.ThreadPoolExecutor(max_workers=len(arts_unique)/20)
# Менеджер коннектов к сайту
http = urllib3.PoolManager(10)

#results_www = task_queue(parse_www, arts_unique, executor)

executor = futures.ThreadPoolExecutor(max_workers=len(arts_unique)/20)
results_html = task_queue(parse_html, arts_unique, executor)
cursor.executemany("INSERT INTO html (art, value, price) VALUES (?, ?, ?)", sqls)
connection.commit()
connection.close()

