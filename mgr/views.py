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


# 登录
def sign_in(request):
    userName = request.params['user_name']
    password = request.params['password']

    # 检查是否存在该用户
    try:
        user = UserInfo.objects.get(userName=userName)
        print('1')
    except UserInfo.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户名或密码错误！'})

    # 检查密码是否正确
    if not check_password(password, user.password):
        return JsonResponse({'ret': 1, 'msg': '用户名或密码错误！'})

    return JsonResponse({'ret': 0, 'user': serializers.serialize("json", [user])[1:-1], 'msg': 0})


# 注册
def register(request):
    userName = request.params['user_name']

    try:
        # 检查是否存在该用户
        user = UserInfo.objects.get(userName=userName)
    except UserInfo.DoesNotExist:
        pass
    # 检查用户名格式
    if not re.match('^[\u4e00-\u9fa5_a-zA-Z0-9]+$', userName):
        return JsonResponse({'ret': 1, 'msg': '用户名为中文英文数字及下划线组成。'})

    # 检查密码格式及加密
    password = request.params['password']
    if not re.match(r'[0-9]{6}', password):
        return JsonResponse({'ret': 1, 'msg': '密码需为六位数字！'})
    password = make_password(password)

    mailbox = request.params['mailbox']
    if not re.match('^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$', mailbox):
        return JsonResponse({'ret': 1, 'msg': '邮箱格式不正确！'})

    birth = datetime.strptime(request.params['birth'], "%Y-%m-%d")

    with transaction.atomic():
        # 创建用户
        user = UserInfo.objects.create(
            userName=userName,
            password=password,
            birth=birth,
            balance=request.params['balance'],
            mailbox=mailbox,
            mgr=1
        )

    return JsonResponse({'ret': 0, 'user': serializers.serialize("json", [user])[1:-1], 'msg': '创建成功！'})


# 修改用户资料
def change_info(request):
    userId = request.params['id']
    user = UserInfo.objects.get(userId=userId)
    user.userName = request.params['user_name']
    user.birth = datetime.strptime(request.params['birth'], "%Y-%m-%d")
    user.mailbox = request.params['mailbox']
    user.balance = request.params['balance']
    user.save()


# 函数字典
ActionHandler = {
    'sign_in': sign_in,
    'register': register,

}


def dispatcher(request):
    return dispatcherBase(request, ActionHandler)
