from .models import *


def custom_proc(request):
    tags = Tag.objects.all()
    catagories = Catagory.objects.all()
    archives = Archive.objects.all()
    articles_rank = Article.objects.prefetch_related()
    articles_rank = sorted(articles_rank, key=lambda a: len(a.readrecord_set.all()), reverse=True)[:10]
    article_sum = sum([catagory.article_quan for catagory in catagories])
    links = Link.objects.all()

    return {'tags': tags, 'catagories': catagories, 'archives': archives, 'sum': article_sum, 'rank': articles_rank,
            'links': links}
