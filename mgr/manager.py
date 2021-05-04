# -*-coding:utf-8-*-
import re
from datetime import datetime
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from lib.handler import dispatcherBase
from common.models import UserInfo
from django.db import transaction
from django.core import serializers


# 列出用户
def list_users(request):
    try:
        qs = UserInfo.objects.values()
    except UserInfo.DoesNotExist:
        return JsonResponse({'ret':1,'msg':'没有用户存在，请添加！'})
    qs = list(qs)

    return JsonResponse({'ret':0,'retlist':qs,'msg':''})


# 按用户名查询用户
def query_user_by_name(request):
    userName = request['user_name']
    try:
        user =  UserInfo.objects.values().filter(userName=userName)
    except UserInfo.DoesNotExist:
        return JsonResponse({'ret':1,'msg':'用户名不存在，请重新输入！'})

    return JsonResponse({'ret': 0, 'user': serializers.serialize("json", [user])[1:-1], 'msg': ''})


# 按ID查询用户
def query_user_by_id(request):
    userId = request['id']
    try:
        user =  UserInfo.objects.values().filter(userId=userId)
    except UserInfo.DoesNotExist:
        return JsonResponse({'ret':1,'msg':'用户名不存在，请重新输入！'})

    return JsonResponse({'ret': 0, 'user': serializers.serialize("json", [user])[1:-1], 'msg': ''})


# 修改用户资料
def change_info(request):
    userId = request.params['id']
    user = UserInfo.objects.get(userId=userId)

    password = request.params['password']
    user.password = make_password(password)
    user.userName = request.params['user_name']
    user.birth = datetime.strptime(request.params['birth'], "%Y-%m-%d").date()
    user.mailbox = request.params['mailbox']
    user.balance = request.params['balance']
    user.save()

    return JsonResponse({'ret': 0, 'user': serializers.serialize("json", [user])[1:-1], 'msg': '修改信息成功！'})


# 删除用户
def delete_user(request):
    userId = request.params['id']
    with transaction.atomic():
        UserInfo.objects.filter(userId=userId).delete()

    return JsonResponse({'ret':0,'msg':''})


# 函数字典
ActionHandler = {
    'list_users':list_users,
    'query_user_by_name':'query_user_by_name',
    'query_user_by_id': 'query_user_by_id',
    'change_info': 'change_info',
    'delete_user':'delete_user'
}


def dispatcher(request):
    return dispatcherBase(request, ActionHandler)