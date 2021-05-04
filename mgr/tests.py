from django.test import TestCase

# Create your tests here.
import requests, pprint

# 请求数据
payload = {'id': 4, 'action': 'change_info', 'user_name': '洛天依', 'password': '000000', 'old_password': '000000',
           'new_password': '123456',
           'birth': '2005-06-17', 'mailbox': 'luotianyi@qq.com', 'balance': 50000}
payload = {'id': 4, 'action': 'edit_article', 'title': '关于程序员通宵写代码这件事','ptitle': '《关于程序员通宵写代码这件事》', 'content': '电脑都不休息，人凭什么休息'}

# 响应内容
response = requests.post("http://127.0.0.1:8000/mgr/articles", json=payload)

getload = {"action": 'query_user_article', 'title':'关于程序员通宵写代码这件事','id':4,'user_name': '洛天依', 'password': '000000', 'pagenum': 1, 'pagesize': 5}

# response = requests.get("http://127.0.0.1:8000/mgr/articles", params=getload)
# 引用pprint结构化输出数据
pprint.pprint(response.json())
