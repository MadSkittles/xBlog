# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xBlog', '0005_auto_20160323_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
