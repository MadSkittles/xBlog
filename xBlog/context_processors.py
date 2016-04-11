from .models import *
from django.db import connection


def custom_proc(request):
    tags = Tag.objects.all()
    catagories = Catagory.objects.all()
    archives = Archive.objects.all()
    articles_rank = Article.objects.prefetch_related()
    articles_rank = sorted(articles_rank, key=lambda a: len(a.readrecord_set.all()), reverse=True)[:10]
    article_sum = sum([catagory.article_quan for catagory in catagories])
    links = Link.objects.all()

    csrf_token = None

    if 'csrftoken' in request.COOKIES:
        csrf_token = request.COOKIES['csrftoken']

    return {'tags': tags, 'catagories': catagories, 'archives': archives, 'sum': article_sum, 'rank': articles_rank,
            'links': links, 'csrf_token': csrf_token}
