#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request,session,flash,g,jsonify
from flask import redirect, url_for,escape
from flask import make_response
from datetime import timedelta
import service.myservice

# 实例化，可视为固定格式
app = Flask(__name__)

# session 需要
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# route()方法用于设定路由；类似spring路由配置
#等价于在方法后写：app.add_url_rule('/', 'helloworld', hello_world)
@app.route('/')
def index():
    if 'loginName' in session:
        return render_template("main.html")
    return 'Hello, World!'

# 配置路由，当请求get.html时交由get_html()处理
@app.route('/login.html')
def login():
    # 使用render_template()方法重定向到templates文件夹下查找login.html文件
    loginName = request.args.get('loginName', '')
    #return render_template('login.html',errorMsg=msg)
    return render_template('login.html',loginName=loginName)


# 配置路由，当请求deal_request时交由deal_request()处理
# 默认处理get请求，我们通过methods参数指明也处理post请求
# 当然还可以直接指定methods = ['POST']只处理post请求, 这样下面就不需要if了
@app.route('/login', methods = ['GET', 'POST'])
def doLogin():
    loginName = ""
    password = ""
    
    if request.method == "GET":
        # get通过request.args.get("param_name","")形式获取参数值
        loginName = request.args.get("loginName","")
        password = request.args.get("password","")
    elif request.method == "POST":
        # post通过request.form["param_name"]形式获取参数值
        loginName = request.form["loginName"]
        password = request.form["password"]
        result = service.myservice.doLogin(loginName,password)

    if(result):
        session['loginName'] = loginName
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5) # 设置session到期时间
        return redirect(url_for('index'))
    else:
        flash('用户名密码错误！')
        return redirect(url_for('login',loginName=loginName))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('loginName', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    app.logger.error(error)
    if request.path.startswith('/api/'):
        return jsonify(error=str(error)),200
    return render_template('404.html'), 200

@app.route("/me")
def me_api():
    return {
        "username": "test",
        "theme": "usertheme"
    }

# export FLASK_APP=myapp.py
# flask run
# 如果使用上面的命令，可以不写下面的程序入口。
if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(debug=True)