# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xBlog', '0008_visitor_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='data_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
