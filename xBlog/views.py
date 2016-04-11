from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response, render
from django.utils import timezone

from .models import *
# from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.db.models import Q
from .IpInfo import *
from django.core.cache import cache
from .MailReminder import send_mail
import threading


# Create your views here.
def home(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        posts = Article.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).prefetch_related()
        result_num = len(posts)
    else:
        posts = Article.objects.prefetch_related()
        keyword = None
        result_num = 0

    page = request.GET.get('page')

    paginator = Paginator(posts, 8)
    records = ReadRecord.objects.all().order_by('-date_time')[:5]
    comments = Comment.objects.all().order_by('-submit_time')[:5]
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render_to_response('xBlog/articles.html', {'post_list': post_list, 'records': records, 'comments': comments,
                                                      'record_sum': len(comments), 'keyword': keyword,
                                                      'result_num': result_num},
                              context_instance=RequestContext(request))


def get_detail(request, article_id):
    ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META[
        'REMOTE_ADDR']

    visitor = get_visitor(ip)

    try:
        article = Article.objects.prefetch_related().select_related().get(pk=article_id)

        article_suggest = Article.objects.filter(Q(catagory=article.catagory) & ~Q(pk=article.id)).order_by('?')[:4]

        previous_articles = Article.objects.filter(pk__lt=article_id).order_by('-pk')
        next_articles = Article.objects.filter(pk__gt=article_id).order_by('pk')

        p_article = previous_articles[0] if len(previous_articles) else None
        n_article = next_articles[0] if len(next_articles) else None

        try:
            record = ReadRecord.objects.get(Q(article=article) & Q(visitor=visitor))
        except ReadRecord.DoesNotExist:
            ReadRecord.objects.create(article=article, visitor=visitor)
        else:
            record.date_time = timezone.now()
            record.save()

        records = article.readrecord_set.all().order_by('-date_time')[:4]

    except Article.DoesNotExist:
        raise Http404
    return render_to_response('xBlog/detail.html',
                              {'article': article, 'suggest': article_suggest, 'previous': p_article, 'next': n_article,
                               'records': records}, context_instance=RequestContext(request))


def get_tag_list(request, tag_name):
    try:
        tag = Tag.objects.get(tag_name=tag_name)
    except Article.DoesNotExist:
        raise Http404
    posts = tag.article_set.all()
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render_to_response('xBlog/articles.html', {'post_list': post_list}, context_instance=RequestContext(request))


def get_archive_list(request, archive_name):
    try:
        archive = Archive.objects.prefetch_related().get(archive_name=archive_name)
    except Article.DoesNotExist:
        raise Http404
    posts = archive.article_set.all()
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render_to_response('xBlog/articles.html', {'post_list': post_list}, context_instance=RequestContext(request))


def get_catagory_list(request, catagory_name):
    try:
        catagory = Catagory.objects.prefetch_related().get(catagory_name=catagory_name)
    except Article.DoesNotExist:
        raise Http404
    posts = catagory.article_set.all()
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render_to_response('xBlog/articles.html', {'post_list': post_list}, context_instance=RequestContext(request))


def alipay(request):
    return render(request, 'xBlog/alipay.html', context_instance=RequestContext(request))


def resume(request):
    return render(request, 'xBlog/resume.html', context_instance=RequestContext(request))


def submit_comment(request, article_id):
    if request.method == 'POST':
        ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META[
            'REMOTE_ADDR']

        visitor = get_visitor(ip)

        nickname = request.POST.get('nickname') or None
        email = request.POST.get('email') or None
        url = request.POST.get('url') or None

        visitor.nickname = nickname or visitor.nickname
        visitor.email = email or visitor.email
        visitor.url = url or visitor.url
        visitor.save()

        content = request.POST.get('content')
        reply_to_who_id = request.POST.get('reply_to_who_id')

        if reply_to_who_id != 'null':
            reply_to_comment = Comment.objects.select_related().get(pk=reply_to_who_id)

            if reply_to_comment.visitor.email:
                threading.Thread(target=send_mail,
                                 args=(visitor, reply_to_comment.visitor, reply_to_comment.article_id)).start()

            reply_to = '回复 #' + str(reply_to_comment.comment_id) + ' ' + reply_to_comment.visitor.nickname + ip_protect(
                reply_to_comment.visitor.ip_address) + '[' + reply_to_comment.visitor.city + ']'
        else:
            reply_to = ''

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

        comment = Comment()
        comment.article_id = article
        comment.nickname = nickname
        comment.email = email
        comment.url = url
        comment.visitor = visitor
        comment.content = content

        if reply_to_who_id != 'null':
            comment.reply_to_who_id = Comment.objects.get(pk=reply_to_who_id)
            comment.reply_to = reply_to

        comment.save()

        result = dict()
        result['author'] = visitor.nickname + ip_protect(visitor.ip_address) + '[' + visitor.city + ']'
        result['id'] = comment.id
        result['author_id'] = comment.visitor.id
        result['url'] = visitor.url
        result['content'] = content
        result['submit_time'] = timezone.localtime(comment.submit_time).strftime('%Y-%m-%d %H:%M')

        if comment.reply_to_who_id:
            result['reply_to_id'] = comment.reply_to_who_id.comment_id
            result['reply_to'] = reply_to

        # print('nickname: ', comment.nickname, 'reply: ', comment.reply_to,
        #       '/', 'content: ', comment.content, '/', comment.comment_id)
        return JsonResponse(result)
    else:
        raise Http404


def today_visitors(request):
    if request.method == 'POST':
        import pytz
        date = timezone.now().strftime('%Y/%m/%d')
        date_begin = timezone.datetime.strptime(date, '%Y/%m/%d').replace(tzinfo=pytz.utc)
        date_end = timezone.datetime.strptime(date + ' 23:59:59', '%Y/%m/%d %H:%M:%S').replace(tzinfo=pytz.utc)
        vistiors = Visitor.objects.filter(Q(data_time__lt=date_end) & Q(data_time__gt=date_begin))

        data = []
        for v in vistiors:
            data.append({'nickname': v.nickname,
                         'date_time': v.data_time.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%H:%M')})

        return JsonResponse({'data': data})
    else:
        return Http404


def online_visitors(request):
    if request.method == 'POST':
        online_ips = cache.get("online_ips", [])

        if online_ips:
            online_ips = list(cache.get_many(online_ips).keys())

        vistiors = Visitor.objects.filter(ip_address__in=online_ips)
        import pytz
        data = []
        for v in vistiors:
            data.append({'nickname': v.nickname,
                         'date_time': v.data_time.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%H:%M')})

        return JsonResponse({'data': data})
    else:
        return Http404


def get_visitor(ip):
    try:
        visitor = Visitor.objects.get(ip_address=ip)
    except Visitor.DoesNotExist:
        visitor = Visitor()
        ip_location = get_ip_info(ip)
        city = ip_location['city'] or ip_location['country']
        city = city[:city.index('市')] if '市' in city else city
        city = '本地' if city == '未分配或者内网IP' else city
        visitor.nickname = '网友'
        visitor.ip_address = ip
        visitor.city = city
        visitor.save()
    else:
        visitor.data_time = timezone.now()
        visitor.save()

    return visitor
