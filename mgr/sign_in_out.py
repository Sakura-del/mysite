# -*-coding:utf-8-*-
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from lib.handler import dispatcherBase
from common.models import UserInfo
from django.db import transaction


# 登录
def sign_in(request):
    userName = request.params['user_name']
    password = request.params['password']

    # 检查是否存在该用户
    try:
        user = UserInfo.objects.get(userName=userName)
    except UserInfo.DoesNotExist:
        return JsonResponse({'ret':0,'msg':'用户名或密码错误！'})

    # 检查密码是否正确
    if check_password(password,user.password):
        return JsonResponse({'ret':0,'msg':'用户名或密码错误！'})

    return JsonResponse({'ret':0,'user':user, 'msg':0})


# 登出
def sign_out(request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})

# 函数字典
ActionHandler = {
    'sign_in':sign_in,
    'sign_out':sign_out
}


def dispatcher(request):
    return dispatcherBase(request, ActionHandler)