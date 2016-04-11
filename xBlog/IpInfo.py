from urllib.request import build_opener
import json


def get_ip_info(ip):
    apiUrlTaobao = 'http://ip.taobao.com/service/getIpInfo.php?ip='
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    opener = build_opener()
    opener.addheaders = [headers]
    data = opener.open(apiUrlTaobao + ip).read()
    data = data.decode('UTF-8')
    data = json.loads(data)['data']
    return {'country': data['country'], 'region': data['region'], 'city': data['city']}


def ip_protect(ip):
    first = ip.index('.')
    last = ip.rindex('.')
    return ip[:first] + '.*.*.' + ip[last + 1:]