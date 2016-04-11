from django.db import models
from django.core.urlresolvers import reverse
import datetime


def get_default_archive():
    return datetime.datetime.now().strftime('%Y-%m')


# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    article_quan = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.tag_name


class Catagory(models.Model):
    catagory_name = models.CharField(max_length=100)
    article_quan = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.catagory_name


class Archive(models.Model):
    archive_name = models.CharField(max_length=50, default=get_default_archive)
    article_quan = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.archive_name


class Article(models.Model):
    title = models.CharField(max_length=100)
    catagory = models.ForeignKey(Catagory, null=True)
    tags = models.ManyToManyField(Tag)
    archive = models.ForeignKey(Archive, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_exists = Article.objects.filter(pk=self.pk)
        super(Article, self).save(force_insert, force_update, using, update_fields)
        if not is_exists:
            self.catagory.article_quan += 1
            self.catagory.save()
            self.archive.article_quan += 1
            self.archive.save()
            # self.tags.article_quan += 1
            # self.tags.save()

    def get_absolute_url(self):
        path = reverse('article', kwargs={'articleid': self.id})
        return path

    # objects = ArticleManager()
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class Link(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Visitor(models.Model):
    nickname = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True)
    data_time = models.DateTimeField(auto_now_add=True, null=True)
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.ip_address


class ReadRecord(models.Model):
    visitor = models.ForeignKey(Visitor)
    article = models.ForeignKey(Article)
    date_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    article_id = models.ForeignKey(Article, null=False)
    visitor = models.ForeignKey(Visitor, null=True)
    content = models.TextField(blank=True)
    reply_to_who_id = models.ForeignKey('self', null=True)
    reply_to = models.CharField(max_length=150, null=True)
    submit_time = models.DateTimeField(auto_now_add=True)
    comment_id = models.IntegerField(default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        comments = Comment.objects.filter(article_id=self.article_id).order_by('-comment_id')
        cid = 1
        if comments:
            cid = comments[0].comment_id + 1

        self.comment_id = cid
        super(Comment, self).save()

    def __str__(self):
        return self.article_id.title + '@' + self.visitor.nickname + '@' + self.submit_time.strftime('%Y-%m-%d %H:%M')
