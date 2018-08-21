import time as tm
import os
from  bs4 import BeautifulSoup
from pymongo import MongoClient
from gets import gets
# coding=utf-8
import smtplib
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


def mailSend():  

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
    content = content + "</table>"
    body = content

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

        # 密码纠错功能(整合自动补全成绩信息数据库功能)(其实也可以封装成一个函数的)
        # 先切换一下数据集合
        col = db["students"]
        # 实现成绩信息自动补全
        info_find = col.find({"user_id":user_id})
        if info_find.count() == 0:
            try:
                info_add = gets(user_id, passwordd)
                col.insert(info_add)
                print("学号为{}的成绩数据添加成功".format(user_id)) # 添加成功表明了学号和密码都是正确的
            except:
                content = """
            	    <h1>您在订阅服务中输入的学号或密码有误,请返回成绩查询系统重新订阅(本消息只发送一次,这个错误的订阅数据将会被删除)</h1>
            	    """
                body = content
                send(user_id, password, email, body)
            	    # 切换数据集合删东西啦啦啦
                col = db["email"]
                target = col.find({"user_id":user_id})
                target_id = target[0]["_id"]
                col.remove({'_id':target_id})
                print("错误订阅数据删除成功")
                continue # 直接去下一次循环咯
                # 接下来利用成绩数据库验证密码
        elif info_find.count() >= 1:
            col = db["students"]
            if info_find[0]["password"] != password:
                content = """
        	        <h1>您在订阅服务中输入的学号或密码有误,请返回成绩查询系统重新订阅(本消息只发送一次,这个错误的订阅数据将会被删除)</h1>
        	        """
                body = content
                send(user_id, password, email, body)
        	        # 切换数据集合删东西啦啦
                col = db["email"]
                target = col.find({"user_id":user_id})
                target_id = target[0]["_id"]
                col.remove({'_id':target_id})
                print("错误订阅数据删除成功")
                continue # 直接去下一次循环咯
            elif info_find[0]["password"] == password:
                print("学号为{}的订阅用户密码验证通过".format(user_id))

        col = db["thc"]
        # 获取当前最新成绩
        info_new = func(user_id, passwd)
        # 对比成绩信息
        if info_new["成绩"] != info_find[0]["成绩"]:
            # 更新数据库,使用先删除再插入的方法暴力更新
            info_target = col.find({"user_id":user_id})
            info_target_id = target[0]["_id"]
            col.remove({'_id':info_target_id})
            col.insert(info_new)
            # 生成HTML成绩表格
            content = words(user_id, passwd)
            # 发送成绩更新通知邮件
            send(user_id, passwd, email, content)
        elif info_new["成绩"] == info_find[0]["成绩"]:
            print("学号为{}的成绩数据没有更新".format(user_id))

    	        #sendmail(email,body)
    	        #col.update({"user_id": user_id},new_info)
    	        #gets.mailUpdate(user_id, email)
    	        #col.update({"user_id": user_id},{"$set":{"sign":""}})

def main():
    while 1:
        updatemail()
        tm.sleep(100)
if __name__ == "__main__":
        main()
