# -*-coding:utf-8-*-
import re
from datetime import datetime

import jieba
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Q
from django.http import JsonResponse
from lib.handler import dispatcherBase
from common.models import UserInfo, Articles
from django.db import transaction
from django.core import serializers


# 列出用户文章
def list_articles(request):
    try:
        qs = UserInfo.objects.values('userId', 'userName').annotate(articles_count=Count('articles')).order_by(
            'userName')
        # 页数
        pagenum = request.params['pagenum']
        # 页大小
        pagesize = request.params['pagesize']

        pgnt = Paginator(qs, pagesize)
        # 问题总数
        total_articles = pgnt.count

        page = pgnt.page(pagenum)

        page = list(page)

        return JsonResponse(
            {"ret": 0, "retlist": page, 'total_articles': total_articles, "total": len(page), "msg": ""})
    except EmptyPage:
        # 数据查完
        return JsonResponse({'ret': 0, 'total_rumors': [], 'total': 0, "msg": "没有更多数据了"})
    except UserInfo.DoesNotExist:
        # 数据获取失败
        return JsonResponse({"ret": 1, "msg": "信息获取失败"})


# 查询某用户所有文章
def get_user_articles(request):
    userId = request.params['id']
    try:
        articles = Articles.objects.values('articleId','articleTitle', 'articleContent','pubDate').filter(author=userId)
    except Articles.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '该用户尚未发表文章'})

    articles = list(articles)

    return JsonResponse({'ret': 0, 'retlist': articles, 'msg': ''})


# 搜索文章
def query_article(request):
    title = request.params['title']
    try:
        qs = Articles.objects.values('articleId', 'articleTitle', 'articleContent', 'pubDate',
                                     'author__userName', 'author__userId').distinct().order_by('-pubDate')
        stopwords = [
            line.strip() for line in open(
                'search_stopwords.txt', "r", encoding='UTF-8').readlines()
        ]
        # 分词，获取用户输入的关键词
        keywords = jieba.cut(title)
        if keywords:
            conditions = [
                Q(articleTitle__contains=one) for one in keywords if one not in stopwords  # 去除停用词
            ]
        # 引用Q查询
        query = Q()
        for condition in conditions:
            query |= condition
        qs = qs.filter(query)
        # 获取页数
        pagenum = request.params['pagenum']
        # 每页问题数量
        pagesize = request.params['pagesize']
        pgnt = Paginator(qs, pagesize)
        page = pgnt.page(pagenum)
        # 转换为可序列化的列表
        retlist = list(page)

        return JsonResponse({"ret": 0, "retlist": retlist, "total": len(retlist), "msg": ""})

    except EmptyPage:
        # 数据查完
        return JsonResponse({'ret': 0, 'total_articles': [], 'total': 0, "msg": "没有更多数据了"})

    except Articles.DoesNotExist:
        # 数据获取失败
        return JsonResponse({"ret": 1, "msg": "信息获取失败"})


# 查询某用户文章
def query_user_article(request):
    userId = request.params['id']
    title = request.params['title']
    try:
        qs = Articles.objects.values('articleTitle', 'pubDate', 'articleContent').distinct().filter(
            Q(author=userId) & Q(articleTitle=title)).order_by('articleTitle')

        # 获取页数
        pagenum = request.params['pagenum']
        # 每页问题数量
        pagesize = request.params['pagesize']
        pgnt = Paginator(qs, pagesize)
        page = pgnt.page(pagenum)
        # 转换为可序列化的列表
        retlist = list(page)

        return JsonResponse({"ret": 0, "retlist": retlist, "total": len(retlist), "msg": ""})

    except EmptyPage:
        # 数据查完
        return JsonResponse({'ret': 0, 'total_articles': [], 'total': 0, "msg": "没有更多数据了"})

    except Articles.DoesNotExist:
        # 数据获取失败
        return JsonResponse({"ret": 1, "msg": "信息获取失败"})


# 修改文章
def edit_article(request):
    articleId = request.params['articleId']
    try:
        article = Articles.objects.get(Q(articleId=articleId))
    except Articles.DoesNotExist:
        # 数据获取失败
        return JsonResponse({"ret": 1, "msg": "信息获取失败"})

    article.articleTitle = request.params['title']
    article.articleContent = request.params['content']
    article.save()

    qs = Articles.objects.values().filter(articleId=article.articleId)
    qs = list(qs)

    return JsonResponse({'ret': 0, 'user': qs[0], 'msg': '修改成功！'})


# 写文章
def write_article(request):
    userId = request.params['user_id']
    try:
        user = UserInfo.objects.get(userId=userId)
    except UserInfo.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '用户不存在！'})

    with transaction.atomic():
        Articles.objects.create(
            articleTitle=request.params['title'],
            articleContent=request.params['content'],
            author=user,
            pubDate=datetime.now()
        )

    return JsonResponse({'ret': 0, 'msg': '文章发表成功'})


# 删除文章
def delete_article(request):
    articleId = request.params['article_id']
    with transaction.atomic():
        Articles.objects.filter(articleId=articleId).delete()

    return JsonResponse({'ret': 0, 'msg': '文章删除'})


# 函数字典
ActionHandler = {
    'list_articles': list_articles,
    'get_user_articles': get_user_articles,
    'query_article': query_article,
    'query_user_article': query_user_article,
    'edit_article': edit_article,
    'write_article': write_article,
    'delete_article': delete_article
}


def dispatcher(request):
    return dispatcherBase(request, ActionHandler)
