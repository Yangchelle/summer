from flask import Flask,render_template,request,jsonify
from gets import gets #从前面爬虫里拿到后面get函数
from pymongo import MongoClient
import json
from bson import json_util
#BSON有JSON没有的一些数据类型，如Date和BinData类型

app = Flask(__name__)
  
client = MongoClient("locahost",27017)#"192.168.1.148",27017)
db = client["mydb"]
col = db["students"]   


def Gets(user_id, password):
    info1 = col.find({"学号":user_id})
    print(info1)
    if info1.count() >= 1:
        if info1[0]["password"] == password:
            return json.dumps(info1[0],default=json_util.default)
        else:
             return{}
    elif info1.count() == 0:
        info = Gets(user_id, password)
        col.insert(info)
        return info



@app.route("/",methods=["POST","GET"])
def index():
    # return "hello Yangxue"
    return render_template("index.html")

@app.route("/info",methods=["POST","GET"])
def showinfo():
    if request.method=="GET":
        content="请填写正确的信息"
        return render_template("error.html",content=content)
    elif request.method=="POST":
        user_id = request.form["username"]#网页上获取的
        #request语法:
        #用以获取客户端在FORM表单中所输入的信息。（表单的method属性值需要为POST）
        #stra=request.form["strUserld"]
        password = request.form["password"]
        info1 = gets(user_id,password)#爬虫获取的
        return render_template("info1.html",content=info1)
    return render_template("index.html")


@app.route("/api/info",methods=["POST","GET"])
def api_info():
    if request.method=="GET":
        content="请填写正确的信息"
        return str({"message":content})#str强行输出为字符串
    elif request.method=="POST":
        user_id = request.form["username"]
        password = request.form["password"]
        info1 = Gets(user_id,password)
        res = jsonify(info1) 
        res.headers['Access-Control-Allow-Origin'] = '*'.encode("utf-8").decode("latin1")
        res.headers['Access-Control-Allow-Methods'] = 'POST，GET,OPTIONS'.encode("utf-8").decode("latin1")
        res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'.encode("utf-8").decode("latin1")
        return res

@app.errorhandler(404)
def error(e):
    content="404小可爱你地址错啦！"
    return render_template("error.html",content=content)

@app.errorhandler(405)
def error(e):
    content="405傻孩子出错啦！"
    return render_template("error.html",content=content)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=80)

