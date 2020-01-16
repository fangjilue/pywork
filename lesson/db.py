#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import mysql.connector
import requests

def dingding(jsonObject):
    r = requests.post("https://oapi.dingtalk.com/robot/send?access_token=88e8c3fae52d249250d6ddeaa2561a54d77d4a411f3f4724d41d664777fd4f60",headers={"Content-Type": "application/json"},json=jsonObject)
    if(r.status_code == 200):
        print("消息发送成功")
    else:
        print("消息发送失败")

if __name__ == '__main__':

	mydb = mysql.connector.connect(
	  host="172.16.0.8",  # 数据库主机地址
	  user="wy_zhuanyong",    # 数据库用户名
	  passwd="mogojiayou@123",  # 数据库密码
	  database="acct",
	  port="3306"
	)
	 
	mycursor = mydb.cursor()

	sql = "SELECT date_format(sysdate(),'%Y-%m-%d %H:%i:%s') questTime,sum(amount) amount FROM acct.acct_fund WHERE fundType = 101 AND acctid NOT IN (10000, 20000, 10005, 40000, 80000, 1786576218, 10011, 10012, 22450278, 22688207, 22713521, 90000, 1022842611, 1036777937, 1466153334, 1767434826)"
	mycursor.execute(sql)
	myresult = mycursor.fetchone()     # fetchall() 获取所有记录
	data = {"msgtype": "text"}
	data["text"] = {"content": "报警 查询时间:%s , 系统余额:%s元" % (myresult[0],myresult[1])}
	print(data)
	#dingding(data)
	mydb.close()
