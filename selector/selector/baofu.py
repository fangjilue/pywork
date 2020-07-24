#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import pymysql
import requests
#from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

class DB():
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
        # 构造函数建立连接 
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型        
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
        #print("init....")

    def __enter__(self):
        # 返回游标        
        #print("cursor ...")
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行        
        self.conn.commit()
        # 关闭游标        
        self.cur.close()
        # 关闭数据库连接        
        self.conn.close()
        #print("close....")

def dingding(jsonObject):
    r = requests.post("https://oapi.dingtalk.com/robot/send?access_token=e8b6d21dfa827f12d800da5e1b0b47548a1ca5dfbf400394096ce2c50a81ff19",headers={"Content-Type": "application/json"},json=jsonObject)
    if(r.status_code == 200):
        print("消息发送成功")
    else:
        print("消息发送失败")
    #print("httpCode: %s, httpText: %s" % (r.status_code, r.text))

def query(db,sql,begin,end):
    db.execute(sql,(begin,end))
    for rs in db:
        return [rs['num'], rs['total']]

def myjob(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        #宝付-支付成功
        sql ="select count(1) 'num', IFNULL(sum(amount),0) 'total'  from acct.pay_payment t where t.createTime between %s and %s and payChannel ='ALIPAY_MINI_BAOFU' and t.proStatus ='SUCCESS'"
        val = query(db,sql,begin,end)
        txt1 = "支付成功: %s 笔, %s 元" % (val[0],val[1])
        print(txt1)

        #宝付-退款
        sql = "select count(1) 'num', convert(ifnull(sum(refundAmount) / 100, 0),decimal(10,2)) 'total' from pay.pay_refund_record where refundChannel = 'ALIPAY_MINI_BAOFU' and createTime between %s and %s "
        val = query(db,sql,begin,end)
        txt2 = "退款成功: %s 笔, %s 元" % (val[0],val[1])
        print(txt2)

        data["text"]={"content": "汪汪-(%s)宝付交易汇总\n %s \n %s" % (begin,txt1,txt2)}
        data["at"]={"atMobiles": ["17301651261"]}
        print(data)
        #write("%s,%s\n" % (i['questTime'],i['amount']))
        #dingding(data)

def write(str):
    try:
        f = open('blance.txt', 'a+')
        f.write(str)
    finally:
        if f:
            f.close()
        
if __name__ == '__main__':
    #日期
    today = datetime.datetime.now()
    yesterday = today + datetime.timedelta(days = -1)
    tomorrow = today + datetime.timedelta(days = 1)

    #begin 表示查那一天
    begin = today.strftime('%Y-%m-%d')
    end = tomorrow.strftime('%Y-%m-%d')
    myjob(begin,end)

