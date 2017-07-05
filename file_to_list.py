# -*- coding: utf-8 -*-
filename = raw_input("put path to file? \n")


def file_get_contents(file_name):
    file = open(file_name)
    return file.read()

filecontent = file_get_contents(filename)

dict_from_file_content = filecontent.split()

print u"В файле %s содержится %d слов" % (filename, len(dict_from_file_content))
stat = {word.lower(): 0 for word in dict_from_file_content}
for word in dict_from_file_content:
   stat[word.lower()] += 1

print len(stat)