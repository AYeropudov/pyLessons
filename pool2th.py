# -*- coding: utf-8 -*-
import sqlite3
import urllib
import urllib3
import sys
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from arts import arts
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError
import threading

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
    return


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


# очередь
def task_queue(task, iterator, concurrency=10, on_fail=lambda _: None):
    def submit():
        try:
            obj = next(iterator)
        except StopIteration:
            return
        if result.cancelled():
            return
        stats['delayed'] += 1
        future = executor.submit(task, obj)
        future.obj = obj
        future.add_done_callback(download_done)

    def download_done(future):
        with io_lock:
            submit()
            stats['delayed'] -= 1
            stats['done'] += 1
        if future.exception():
            on_fail(future.exception(), future.obj)
        if stats['delayed'] <= 0:
            stats['finish'] = True
            result.set_result(True)

    def clean_up(_):
        with io_lock:
            executor.shutdown(wait=False)

    io_lock = threading.RLock()
    executor = ThreadPoolExecutor(concurrency)
    result = Future()
    result.stats = stats = {'done': 0, 'delayed': 0, 'finish': False}
    result.add_done_callback(clean_up)

    with io_lock:
        for _ in range(concurrency):
            submit()
    return result

# шаблон URL
url_parse = u"http://www.ozon.ru/?context=search&text={}"
# соединение с БД
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
# Выборка уникальных значений из вводного массива
arts_unique = list(set(arts[0:20]))
# Прогресс бар для индикации работы
progressbar = tqdm(total=len(arts_unique), leave=True)
# Пулл потоков

# Менеджер коннектов к сайту
http = urllib3.PoolManager(10)

results = task_queue(parse_www, iter(arts_unique))
try:
    while not results.stats['finish']:
        try:
            results.result(0.3)
        except TimeoutError:
            pass
        if not results.stats['finish']:
                progressbar.update(len(arts_unique) - (len(arts_unique) - results.stats['done']))
        else:
            progressbar.close()
        # print '\rdone {done}, in work: {delayed}  '.format(**results.stats), sys.stdout.flush()
except KeyboardInterrupt:
    results.cancel()
connection.commit()
cursor.close()
connection.close()

