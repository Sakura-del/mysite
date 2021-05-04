# -*-coding:utf-8-*-
from django.http import JsonResponse
import json


# 请求处理函数
def dispatcherBase(request, ActionHandler):
    if request.method == 'GET':
        request.params = request.GET

    # elif request.method in ['POST', 'PUT', 'DELETE']:
    #     # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
    #     request.params = json.loads(request.body)
    #     print(request.params)

    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        print(request.POST.dict())
        # 将POST请求转字典，再转json
        request.params = json.dumps(request.POST.dict(), ensure_ascii=False)
        request.params = json.loads(request.params)
        print(request.params)

    action = request.params['action']
    if action in ActionHandler:
        handlerFunc = ActionHandler[action]
        return handlerFunc(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'action参数错误'})

