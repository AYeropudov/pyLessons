dict = {
    'key': 'value',
    'key2': 'value2',
    'key3': 'value3'
    }
print dict

dict['count'] = 1
print dict
dict['count'] += 1

print dict

subdict = {}
subdict['title'] = 'Mr.'
subdict['name'] = 'Cheef'
dict['jobTitle'] = subdict

print dict

keys = list(dict.keys())

for key in sorted(keys):
    print(key, ' => ', dict[key])
