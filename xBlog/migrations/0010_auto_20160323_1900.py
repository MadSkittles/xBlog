# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xBlog', '0009_visitor_data_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='article',
        ),
        migrations.AddField(
            model_name='visitor',
            name='articles',
            field=models.ManyToManyField(null=True, to='xBlog.Article'),
        ),
    ]
