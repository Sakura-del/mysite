# Generated by Django 3.1.5 on 2021-05-02 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='userName',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]