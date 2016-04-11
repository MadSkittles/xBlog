from django.contrib import admin
from xBlog.models import *


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ['archive_name', 'article_quan']


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['catagory_name', 'article_quan']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_name', 'article_quan']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'catagory', 'archive', 'date_time']
    list_filter = ['date_time', 'catagory', 'archive', 'tags']
    search_fields = ['title', 'catagory', 'archive', 'tags']
    date_hierarchy = 'date_time'
    filter_horizontal = ['tags']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'link']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article_id', 'visitor', 'reply_to_who_id', 'submit_time', 'comment_id']
    list_filter = ['submit_time', 'article_id']
    search_fields = ['article_id']
    date_hierarchy = 'submit_time'


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'url', 'email', 'ip_address', 'data_time']
    list_filter = ['nickname', 'ip_address']
    date_hierarchy = 'data_time'


@admin.register(ReadRecord)
class ReadRecordAdmin(admin.ModelAdmin):
    list_display = ['article', 'visitor', 'date_time']
    date_hierarchy = 'date_time'
