# -*- coding: utf-8 -*-
import sqlite3

conection = sqlite3.connect('db.sqlite')

filename = raw_input("put path to file? \n")


def dict_factory(c, r):
    t = (r[0], r[1])
    # for i, name in enumerate(c.description):
    return t

conection.row_factory = dict_factory

cursor = conection.cursor()
cursor.execute("SELECT value, count FROM words")

#words_in_db = cursor.fetchall()
stat = cursor.fetchall()
stat = dict(stat)

def file_get_contents(file_name):
    file = open(file_name)
    return file.read()


file_content = file_get_contents(filename)

dict_from_file_content = file_content.split()

print u"В файле %s содержится %d слов" % (filename, len(dict_from_file_content))

for word in dict_from_file_content:
    stat[word.lower()] += 1
print len(stat)

sql = """INSERT OR REPLACE INTO words(value, count) VALUES (?, ?)"""
try:
    cursor.executemany(sql, stat.items())
except sqlite3.DatabaseError as err:
    print u"Ошибка", err
else:
    print u"Запрос успешен"
    conection.commit()
cursor.close()
conection.close()
raw_input("?")
