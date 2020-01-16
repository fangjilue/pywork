#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request
# 添加位置一。从Flask-RESTful中导入以下三项
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse

# 实例化，可视为固定格式
app = Flask(__name__)
# 添加位置二。
# 实例化一个api用于配置rest路由
# 实例化一个参数解析类，用于rest获取get和post提交的参数
api = Api(app)
parser = reqparse.RequestParser()
# 注册q参数parser才能解析get和post中的q参数。这种注册才能解析的要求是否有点孤儿
parser.add_argument('q', type=str, help='Rate to charge for this resource')

# route()方法用于设定路由；类似spring路由配置
#等价于在方法后写：app.add_url_rule('/', 'helloworld', hello_world)
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 配置路由，当请求get.html时交由get_html()处理
@app.route('/get.html')
def get_html():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('get.html')

# 配置路由，当请求post.html时交由post_html()处理
@app.route('/post.html')
def post_html():
    # 使用render_template()方法重定向到templates文件夹下查找post.html文件
    return render_template('post.html')

# 配置路由，当请求deal_request时交由deal_request()处理
# 默认处理get请求，我们通过methods参数指明也处理post请求
# 当然还可以直接指定methods = ['POST']只处理post请求, 这样下面就不需要if了
@app.route('/deal_request', methods = ['GET', 'POST'])
def deal_request():
    if request.method == "GET":
        # get通过request.args.get("param_name","")形式获取参数值
        get_q = request.args.get("q","")
        return render_template("result.html", result=get_q)
    elif request.method == "POST":
        # post通过request.form["param_name"]形式获取参数值
        post_q = request.form["q"]
        return render_template("result.html", result=post_q)

# 添加位置三。
# 添加rest类（是类而不是和Flask一样直接是方法）
class Rest(Resource):
    # get提交时的处理方法
    def get(self):
        result = {}
        args = parser.parse_args()
        result["method"] = "get"
        result["q"] = args["q"]
        return result
    # post提交时的处理方法
    def post(self):
        result = {}
        # 此种方法即可解析通过普通post提交也可解析json格式提交
        args = parser.parse_args()
        result["method"] = "post"
        result["q"] = args["q"]
        return result
# 配置路由
api.add_resource(Rest, '/rest')

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run()