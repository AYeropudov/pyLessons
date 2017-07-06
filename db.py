# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect("db.sqlite")

sql = """
CREATE TABLE user
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    passwd TEXT
);
CREATE TABLE rubr
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
CREATE TABLE site
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER ,
    id_rubr INTEGER ,
    url TEXT,
    title TEXT,
    msg TEXT,
    iq INTEGER ,
    CONSTRAINT site__user_fk FOREIGN KEY (id_user) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT site_rubr_fk FOREIGN KEY (id_rubr) REFERENCES rubr (id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
cursor = con.cursor()

try:
    cursor.executescript(sql)
except sqlite3.DatabaseError as err:
    print u"Ошибка : ", err
else:
    print u"Успешно выполнено"
cursor.close()
con.close()
input()
