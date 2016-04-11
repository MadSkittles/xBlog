import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    return mark_safe(markdown.markdown(value,
                                       extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],
                                       safe_mode=True,
                                       enable_attributes=False))


@register.filter(is_safe=True)
def get_visitor_url(visitor):
    return visitor.url or '/'


@register.filter(is_safe=True)
def sub_content(content, length):
    return content[:length] + ('...' if len(content) > length else '')


@register.filter(is_safe=True)
def ip_protect(ip):
    first = ip.index('.')
    last = ip.rindex('.')
    return ip[:first] + '.*.*.' + ip[last + 1:]
