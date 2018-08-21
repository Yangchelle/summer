from selenium import webdriver
import time as tm 
import requests
import lxml
from  bs4 import BeautifulSoup
from pymongo import MongoClient

Url = "http://jwc3.yangtzeu.edu.cn/eams/login.action"
InfoUrl = "http://jwc3.yangtzeu.edu.cn/eams/stdDetail.action"
GradeUrl = "http://jwc3.yangtzeu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"
user_id = "201706532"

def gets(user_id,password):
    driver = webdriver.PhantomJS()
    driver.get(Url)
    username = driver.find_element_by_id("username").send_keys(user_id)
    passwd = driver.find_element_by_id("password").send_keys(user_id)
    submit = driver.find_element_by_name("submitBtn")
    #username.send_keys(user_id)
    #passwd.send_keys(user_id)
    tm.sleep(1)
    submit.click()
    #print(driver.page_source)
    #抓取学籍信息
    tm.sleep(1)
    driver.get(InfoUrl)
    html = driver.page_source
    #复制粘贴:set paste命令
    #直接粘贴会存在缩进问题
    soup = BeautifulSoup(html, "lxml")
    infos = {}
    keys = []
    vals = []
    trs = soup.find_all("tr")
    for tr in trs[1:-1]:
        tds = tr.find_all("td")
        if len(tds) == 0:    #傻孩子不要再用/*注释了 /*双等号*/
            continue
        key1 = tds[0].getText()[:-1]
        val1 = tds[1].getText()#默认应该是全部取完，用[x：x]限定取的范围
        key2 = tds[2].getText()[:-1]
        val2 = tds[3].getText()
        keys.append(key1)
        keys.append(key2)
        vals.append(val1)
        vals.append(val2)
    for i in range(len(vals)-1):
        infos[keys[i]] = vals[i]
    #print(infos)
    #获取成绩
    #下面两行必须先输入才行，它是先为bs4准备文件，写在soup前
    #tm.sleep(1)#在跳转的时候或者点击的时候用
    tm.sleep(1)
    driver.get(GradeUrl)
    html = driver.page_source
    #以下为复制内容，来源/newbie/Day02/Spider.py
    soup = BeautifulSoup(html,"lxml")
    tables = soup.find_all("table")
    #print(len(tables))
    #print(tables[1])
    point_trs = tables[0].find_all("tr")
    grade_trs = tables[1].find_all("tr")
    point_keys = []
    all_point_keys = ["类型","必修门数","必修学分","必修总绩点"]
    all_point_ths = point_trs[-2].find_all("th")
    grade_keys = []
    grades = []
    points = []
    all_points = []
    all_point = {}
    point = {}
    grade = {}
    
    #print("--------------------")
    time = point_trs[-1].getText().split("2")[1][1:].strip()
    #print(time)
    for idx,all_point_th in enumerate(all_point_ths):
        all_point[all_point_keys[idx]] = all_point_th.getText()
    all_points.append(all_point)
    #print(all_point)
    
    for point_th in point_trs[0].find_all("th"):
        point_keys.append(point_th.getText())
    for grade_th in grade_trs[0].find_all("th"):
        grade_keys.append(grade_th.getText())
    #print(point_keys)
    #print(grade_keys)
    
    for point_tr in point_trs[0:-2]:
        point = {}
        point_tds = point_tr.find_all("td")
        for idx,point_td in enumerate(point_tds):
            point[point_keys[idx]] = point_td.getText()
        points.append(point)
    #print(points)
    
    for grade_tr in grade_trs[1:]:
        grade = {}
        grade_tds = grade_tr.find_all("td")
        for idx,grade_td in enumerate(grade_tds):
            grade[grade_keys[idx]] = grade_td.getText().strip()
        grades.append(grade)
    #print(grades)
    
    #整理数据
    infos["统计时间"] = time
    infos["绩点"] = points
    infos["总绩点"] = all_points
    infos["成绩"] = grades
    infos["user_id"] = user_id
    infos["password"] = password
    return infos
#infos=gets("201706508","201706508")
#print(infos)
'''
    #插入到数据库
    client = MongoClient("locahost",27017)
    #client = MongoClient("locahost",27017)
    db = client["mydb"]
    col1 = db["students"]
    col2 = db["time"]
    col3 = db["point"]
    col4 = db["all_point"]
    col5 = db["grades"]
'''
'''
    col1.insert(infos)
    col2.insert(infos)
    col3.insert(infos)
    col4.insert(infos)
    col5.insert(infos)
    '''

