# -*- coding: utf-8 -*-
import pickle

f = open(r"obj_dump.txt", "wb")
obj = [u"Строка", (2, 4)]
pickle.dump(obj, f)
f.close()

z = open(r"obj_dump.txt", "rb")
parse_obj = pickle.load(z)
print parse_obj
z.close()
