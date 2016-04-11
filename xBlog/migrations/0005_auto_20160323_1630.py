# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 08:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xBlog', '0004_auto_20160322_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100, null=True)),
                ('url', models.CharField(max_length=150, null=True)),
                ('email', models.CharField(max_length=150, null=True)),
                ('content', models.TextField(blank=True)),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('comment_id', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='comment_nums',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='xBlog.Tag'),
        ),
        migrations.AddField(
            model_name='comment',
            name='article_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xBlog.Article'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to_who_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='xBlog.Comment'),
        ),
    ]
