# !/usr/bin/python
# -*-coding:utf-8-*-
import smtplib
from email.mime.text import MIMEText
 
def send_email(host, username, passwd, send_to, subject, content):
    msg = MIMEText(content)
    my_email = username+"<"+username+">"
    msg['From'] = my_email
    msg['Subject'] = subject
    msg['To'] = ",".join(send_to)
 
    try:
        # server = smtplib.SMTP()
        # server.connect(host)
        server = smtplib.SMTP_SSL(host,465)
        server.ehlo()
        # server.starttls()
        server.login(username, passwd)
###第一种方法写的时候遇到了困难，问题没有是有strip()，因为此处使用了 msg.as_string()，应该是将内容转化成了str，然后又进行的处理
        server.sendmail(username, send_to, msg.as_string())
        server.close()
        return 'sucessfully'
    except Exception as e:
        print(e)
        return 'failed to send mail'
 
if __name__ == '__main__':
    #filename = "emails_txt"
    #f = open(filename)
    #lines = f.readlines()
    # file = f.read()
#######################方法1############
###此种方法是在txt文件中配置内容和写文件内容
    """
    host ="smtp.qq.com"
    username = lines[1].split(':')[-1].strip()
    # # host = "smtp." + str(username.split('@')[-1])
    passwd = lines[2].split(':')[-1].strip()
    to_list = lines[3].split(':')[-1].strip().split(',')
    subject = lines[4].split(':')[-1].strip()
    content = lines[5].split(':')[-1]
    # print type(passwd), passwd
    # print type(to_list), to_list
    # print type(subject), subject
    # print type(content), content
    send_email(host, username, passwd, to_list, subject, content)
    """
#######################方法2############
###下面这种方法是在程序中直接写内容，一旦文件内容比较多的时候，就很不适合使用了
    host = 'smtp.exmail.qq.com'
    username = 'fangjilve@mgzf.com'
    #此password为进入QQ邮箱设置页面，开启SMTP服务，发短信获取的授权码，而非通常我们使用的password
    passwd = 'Xr87MK8w6HqhSuXj'
    to_list = ['9432239@qq.com','fang0078@163.com']
    subject = "txt文件发送邮件1"
    content = "用python发送邮件1"
    #content = file
    # print type(passwd), passwd
    # print type(to_list), to_list
    # print type(subject), subject
    # print type(content), content
    if send_email(host, username, passwd, to_list, subject, content):
        print("done!")
    else:
        print("failed!")