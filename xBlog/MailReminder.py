import email.utils
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from MyBlog.settings import MAILUSERNAME, MAILUSERPASSWORD, SMTPSERVERNAME
from .IpInfo import ip_protect


def send_mail(from_visitor, to_visitor, article):
    subject = '大鹌鹑的博客新回复'
    to = to_visitor.email
    date = email.utils.formatdate()

    to_visitor_name = to_visitor.nickname + ip_protect(to_visitor.ip_address) + '[' + to_visitor.city + ']'
    from_visitor_name = from_visitor.nickname + ip_protect(from_visitor.ip_address) + '[' + from_visitor.city + ']'
    text = '%s，您好。%s在文章《%s》中回复了您，点击 http://127.0.0.1:8000/article/%d/#comments 可以查看详细信息。' % (
        to_visitor_name, from_visitor_name, article.title, article.id)

    msg = MIMEText(text, 'text', 'utf-8')
    msg['From'] = MAILUSERNAME
    msg['To'] = to
    msg['Date'] = date
    msg['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP(SMTPSERVERNAME)
    server.login(MAILUSERNAME, MAILUSERPASSWORD)

    failed = server.sendmail(MAILUSERNAME, to, msg.as_string())

    server.quit()
    if failed:
        raise Exception('邮件发送异常')
