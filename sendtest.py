# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
# 发送纯文本格式的邮件
#发送邮箱地址
sender = '15386600824@163.com'
#邮箱授权码，非登陆密码
password = 'yx962464'
#收件箱地址
receiver = '272888672@qq.com'
mailto_list = '272888672@qq.com'#收件人
#smtp服务器
smtp_server = 'smtp.163.com'
#发送邮箱地址

client = MongoClient("localhost", 27017)
db = client["mydb"]
col = db["students"]
info = col.find({"user_id":"201706532"})
grade = {}
if info[0]["password"] == "201706532":
    grade = info[0]
#print(grade)
content = """
<style type="text/css">table{text-align: center;border-collapse:collapse;border: 3px solid;}td,th{border-color: pink;border: 1px solid;}</style><table style="text-align: center;"><tr><th>课程名称</th><th>课程时间</th><th>课程类别</th><th>学分</th><th>最终成绩</th><th>绩点</th></tr>
"""

base = """
<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></td>
"""

for cj in grade.get("成绩"):
    #print(grade.get("成绩"))
    #print(cj)
    content=content+base.format(cj["课程名称"],cj["学年学期"],cj["课程类别"],cj["学分"],cj["总评成绩"],cj["绩点"])
    time = "统计时间" + grade["统计时间"]
    body = content + time + "</table>"
msg = MIMEText(body,'html','utf-8')
msg['From'] = sender
#收件箱地址
msg['To'] = receiver #';'.join(mailto_list)#发送多人邮件写法
#主题 
msg['Subject'] = 'from 成绩查询'
server = smtplib.SMTP(smtp_server,25)# SMTP协议默认端口是25 
server.login(sender,password)#ogin()方法用来登录SMTP服务器 
server.set_debuglevel(1)#打印出和SMTP服务器交互的所有信息。 
server.sendmail(sender,mailto_list,msg.as_string())#msg.as_string()把MIMEText对象变成str server.quit()
# 第一个参数为发送者，第二个参数为接收者，可以添加多个例如：['SunshineWuya@163.com','xxx@qq.com',]# 第三个参数为发送的内容
server.quit()
print("OK!")

