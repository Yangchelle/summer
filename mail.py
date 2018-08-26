import time as tm
import os
from  bs4 import BeautifulSoup
from pymongo import MongoClient
from gets import gets
# coding=utf-8
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import traceback
import hashlib

  
def send(email,body):
	msg = METext(body,'html','utf-8')
#发送邮箱地址
	sender = '15386600824@163.com'
#邮箱授权码，非登陆密码
	password = 'yx962464'
#收件箱地址
	receiver = email
	mailto_list = email #收件人
	mail_body = body
#smtp服务器
	smtp_server = 'smtp.163.com'
#发送邮箱地址
	msg['From'] = sender
#收件箱地址
	msg['To'] = receiver #';'.join(mailto_list)#发送多人邮件写法
#主题 
	msg['Subject'] = 'from 成绩查询'

	try:
		server = smtplib.SMTP(smtp_server,25)# SMTP协议默认端口是25 
		server.login(sender,password)#ogin()方法用来登录SMTP服务器 
		server.set_debuglevel(1)#打印出和SMTP服务器交互的所有信息。 
		server.sendmail(sender,mailto_list,msg.as_string())#msg.as_string()把MIMEText对象变成str server.quit()
# 第一个参数为发送者，第二个参数为接收者，可以添加多个例如：['SunshineWuya@163.com','xxx@qq.com',]# 第三个参数为发送的内容
		server.quit()
		print("OK!")
	except smtplib.SMTPException:
		print("fail!")


def mailSend(user_id,password):
    	# 邮件内容
    client = MongoClient("localhost", 27017)
    db = client["mydb"]
    col = db["students"]
    grade = {}
    grade = gets(user_id,password)
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
    body = content + "</table>"
    send(email,body)
    col.update({"user_id": user_id},new_info)

    return body

def updatemail():
    client = MongoClient("localhost", 27017)
    db = client["mydb"]
    col = db["mail"]
    for info in col.find():
        print(info)
        user_id = info["user_id"]
        password = info["password"]
        email = info["email"]
        col = db["students"]
        info_find = col.find({"user_id":user_id})
        col = db["thc"]
        # 获取当前最新成绩
        info_new = gets(user_id, password)
        # 对比成绩信息
        if info_new["成绩"] != info_find[0]["成绩"]:
            info_target = col.find({"user_id":user_id})
            info_target_id = target[0]["_id"]
            col.remove({'_id':info_target_id})
            col.insert(info_new)
            body = send(user_id, passwd)
            send(user_id, password, email, body)
        elif info_new["成绩"] == info_find[0]["成绩"]:
            print("学号为{}的成绩数据没有更新".format(user_id))

def main():
    while 1:
        mailSend()
        tm.sleep(100)
if __name__ == "__main__":
        main()
