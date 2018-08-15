# coding=utf-8
import smtplib
from email.mime.text import MIMEText
# 发送纯文本格式的邮件
msg = MIMEText('<html><h1>人生苦短，我用python</html></h1>','html','utf-8')
#发送邮箱地址
sender = '15386600824@163.com'
#邮箱授权码，非登陆密码
password = 'yx962464'
#收件箱地址
receiver = '272888672@qq.com'
#mailto_list = '272888672@qq.com'#收件人
#smtp服务器
smtp_server = 'smtp.163.com'
#发送邮箱地址
msg['From'] = sender
#收件箱地址
msg['To'] = receiver #';'.join(mailto_list)#发送多人邮件写法
#主题 
msg['Subject'] = 'from 成绩查询'

server = smtplib.SMTP(smtp_server,25)# SMTP协议默认端口是25 
server.login(sender,password)#ogin()方法用来登录SMTP服务器 
server.set_debuglevel(1)#打印出和SMTP服务器交互的所有信息。 
server.sendmail(sender,receiver,msg.as_string())#msg.as_string()把MIMEText对象变成str server.quit()
# 第一个参数为发送者，第二个参数为接收者，可以添加多个例如：['SunshineWuya@163.com','xxx@qq.com',]# 第三个参数为发送的内容
server.quit()
print("ok")


