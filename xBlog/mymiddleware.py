from .models import Visitor
from .IpInfo import *
from django.utils import timezone
from django.core.cache import cache


class VisitorMiddleware:
    def process_request(self, request):
        ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META[
            'REMOTE_ADDR']
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

        online_ips = cache.get("online_ips", [])

        if online_ips:
            online_ips = list(cache.get_many(online_ips).keys())

        cache.set(ip, 0, 5 * 60)

        if ip not in online_ips:
            online_ips.append(ip)

        cache.set("online_ips", online_ips)
