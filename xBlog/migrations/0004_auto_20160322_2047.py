# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-22 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xBlog', '0003_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(null=True, to='xBlog.Tag'),
        ),
    ]
