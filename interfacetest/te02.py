from urllib import parse
import hashlib

import base64
str = '123456'
obj = {"username":"aba","password":"123456"}
print(parse.quote(str))
# print(base64.b64encode(str))
print(parse.urlencode(obj))

m = hashlib.md5()
m.update('123456'.encode('utf-8'))
m.update('123456'.encode())
sec = m.hexdigest()
print(sec)
