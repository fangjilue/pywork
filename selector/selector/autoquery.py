#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import pymysql
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

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
    r = requests.post("https://oapi.dingtalk.com/robot/send?access_token=88e8c3fae52d249250d6ddeaa2561a54d77d4a411f3f4724d41d664777fd4f60",headers={"Content-Type": "application/json"},json=jsonObject)
    if(r.status_code == 200):
        print("消息发送成功")
    else:
        print("消息发送失败")
    #print("httpCode: %s, httpText: %s" % (r.status_code, r.text))

def myjob():
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='wy_zhuanyong',passwd='mogojiayou@123',db='acct') as db:
        sql = "SELECT date_format(sysdate(),'%Y-%m-%d %H:%i:%s') questTime,sum(amount) amount FROM acct.acct_fund WHERE fundType = 101 AND acctid NOT IN (10000, 20000, 10005, 40000, 80000, 1786576218, 10011, 10012, 22450278, 22688207, 22713521, 90000, 1022842611, 1036777937, 1466153334, 1767434826)"
        db.execute(sql)
        #print(db)
        for i in db:
            data["text"]={"content": "报警 查询时间:%s , 系统余额:%s元" % (i['questTime'],i['amount'])}
            print(data)
            #dingding(data)
        
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    #scheduler.add_job(myjob, 'cron', day=1, hour=0, minute=0,second=0)
    #scheduler.add_job(myjob, 'cron', hour=17,minute=0,second=0)
    scheduler.add_job(myjob, 'interval', seconds=5)
    scheduler.start()
