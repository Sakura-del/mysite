from django.test import TestCase

# Create your tests here.
import requests, pprint

# 请求数据
payload = {'action': 'register', 'user_name': '洛天依', 'password': '000000', 'birth': '2015-01-17',
           'mailbox': 'luotianyi@qq.com','balance':5000}
# 响应内容
response = requests.post("http://127.0.0.1:8000/mgr/views", json=payload)

getload = {"action": 'sign_in', 'user_name': 'Sakura', 'password': '000000'}

response = requests.get("http://127.0.0.1:8000/mgr/views", params=getload)
# 引用pprint结构化输出数据
pprint.pprint(response.json())