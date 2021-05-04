from django.db import models

# Create your models here.


# 用户信息
class UserInfo(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    mailbox = models.CharField(max_length=200)
    birth = models.DateField(auto_now_add=False)
    balance = models.FloatField()
    mgr = models.IntegerField()

    class Meta:
        db_table='user_info'


# 文章
class Articles(models.Model):
    author = models.ForeignKey(UserInfo,on_delete=models.CASCADE,default='')
    articleId = models.AutoField(primary_key=True)
    articleTitle = models.CharField(max_length=200)
    articleContent = models.TextField()
    pubDate = models.DateField(auto_now_add=True)

    class Meta:
        db_table='articles'