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

def mergeList(list1,list2):
    tmp =[]
    if (len(list1) ==0 and len(list2) == 0) :
        return tmp
    elif (len(list1) ==0) :
        return list2
    elif (len(list2) ==0) :
        return list1
    else:
        tmp.extend(list1)
        tmp.extend(list2)
        return tmp

def baofu(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        #宝付-支付成功
        sql ="select count(1) 'num', IFNULL(sum(amount),0) 'total'  from acct.pay_payment t where t.createTime between %s and %s and payChannel ='ALIPAY_MINI_BAOFU' and t.proStatus ='SUCCESS'"
        val = query(db,sql,begin,end)
        txt1 = "支付成功: %s 笔, %s 元" % (val[0],val[1])
        #print(txt1)

        #宝付-退款
        sql = "select count(1) 'num', convert(ifnull(sum(refundAmount) / 100, 0),decimal(10,2)) 'total' from pay.pay_refund_record where refundChannel = 'ALIPAY_MINI_BAOFU' and createTime between %s and %s "
        val = query(db,sql,begin,end)
        txt2 = "退款成功: %s 笔, %s 元" % (val[0],val[1])
        #print(txt2)

        data["text"]={"content": "汪汪-(%s)宝付交易汇总\n %s \n %s" % (begin,txt1,txt2)}
        data["at"]={"atMobiles": ["17301651261"]}
        print(data)
        #write("%s,%s\n" % (i['questTime'],i['amount']))
        #dingding(data)

def tp(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        
        #通联TP
        sql ='''
            SELECT trxcode payChannel,
                   case trxcode
                     when 'VSP501' then '微信'
                     when 'VSP511' then '支付宝'
                     else '其他'
                   end channel,
                   count(1) num ,
                   convert(ifnull(sum(trxamt) / 100, 0),decimal(10,2)) total
            from pay.pay_log_allinpay_alipay_wap t
            where t.paytime between %s and %s
              and t.appid = '00185864'
            group by trxcode
        '''
        
        db.execute(sql,(begin,end))
        rs1 = db.fetchall()
        #print(type(rs1))

        sql = '''
            SELECT tt.payChannel,
                   case tt.payChannel
                     when 'ALIPAY_APP_ALLINPAY' then '支付宝app'
                     when 'WECHAT_MINI_ALLINPAY' then '微信小程序'
                     when 'WECHAT_WAP_ALLINPAY' then '微信wap'
                     when 'ALIPAY_WAP_ALLINPAY' then '支付宝wap'
                     else '其他'
                     end                     channel,
                   count(1)                  num,
                   ifnull(sum(tt.amount), 0) total
            FROM acct.pay_payment tt
            where exists(select 1
                         from pay.pay_log_allinpay_alipay_wap t1
                         WHERE t1.paytime between %s and %s
                           AND t1.trxstatus = '0000'
                           and t1.appid is null
                           and tt.mogoTradeNo = t1.outtrxid)
              and tt.payGatewayId = '00185864'
              and tt.proStatus = 'SUCCESS'
            group by tt.payChannel
        '''
        
        db.execute(sql,(begin,end))
        rs2 = db.fetchall()
        #print(type(rs2))

        rs = mergeList(rs1, rs2)
        #print(rs)

        wenxin_num,wenxin_total=0,0
        alipay_num,alipay_total=0,0
        for i in rs:
            if(i['payChannel'] == 'VSP511' or i['payChannel'] == 'ALIPAY_APP_ALLINPAY' or i['payChannel'] == 'ALIPAY_WAP_ALLINPAY'):
                alipay_num   += i['num']
                alipay_total += i['total']
            elif(i['payChannel'] == 'VSP501' or i['payChannel'] == 'WECHAT_MINI_ALLINPAY' or i['payChannel'] == 'WECHAT_WAP_ALLINPAY'):
                wenxin_num  +=  i['num']
                wenxin_total += i['total']
            else:
                print('payChannel is undefined')
                pass

        txt1 = "微信: %s 笔, %s 元" % (wenxin_num,wenxin_total)
        txt2 = "支付宝: %s 笔, %s 元" % (alipay_num,alipay_total)

        data["text"]={"content": "汪汪-(%s)通联梯辟交易汇总: %s 笔, %s 元 \n %s \n %s" % (begin, wenxin_num+alipay_num, wenxin_total+alipay_total, txt1, txt2)}
        print(data)
        #dingding(data)

def tl(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        
        #通联TP
        sql ='''
            SELECT trxcode payChannel,
                   case trxcode
                     when 'VSP501' then '微信'
                     when 'VSP511' then '支付宝'
                     else '其他'
                   end channel,
                   count(1) num ,
                   convert(ifnull(sum(trxamt) / 100, 0),decimal(10,2)) total
            from pay.pay_log_allinpay_alipay_wap t
            where t.paytime between %s and %s
              and t.appid = '00170896'
            group by trxcode
        '''
        
        db.execute(sql,(begin,end))
        rs1 = db.fetchall()
        #print(type(rs1))

        sql = '''
            SELECT tt.payChannel,
                   case tt.payChannel
                     when 'ALIPAY_APP_ALLINPAY' then '支付宝app'
                     when 'WECHAT_MINI_ALLINPAY' then '微信小程序'
                     when 'WECHAT_WAP_ALLINPAY' then '微信wap'
                     when 'ALIPAY_WAP_ALLINPAY' then '支付宝wap'
                     else '其他'
                     end                     channel,
                   count(1)                  num,
                   ifnull(sum(tt.amount), 0) total
            FROM acct.pay_payment tt
            where exists(select 1
                         from pay.pay_log_allinpay_alipay_wap t1
                         WHERE t1.paytime between %s and %s
                           AND t1.trxstatus = '0000'
                           and t1.appid is null
                           and tt.mogoTradeNo = t1.outtrxid)
              and tt.payGatewayId = '00170896'
              and tt.proStatus = 'SUCCESS'
            group by tt.payChannel
        '''
        
        db.execute(sql,(begin,end))
        rs2 = db.fetchall()
        #print(type(rs2))

        rs = mergeList(rs1, rs2)
        #print(rs)

        wenxin_num,wenxin_total=0,0
        alipay_num,alipay_total=0,0
        for i in rs:
            if(i['payChannel'] == 'VSP511' or i['payChannel'] == 'ALIPAY_APP_ALLINPAY' or i['payChannel'] == 'ALIPAY_WAP_ALLINPAY'):
                alipay_num   += i['num']
                alipay_total += i['total']
            elif(i['payChannel'] == 'VSP501' or i['payChannel'] == 'WECHAT_MINI_ALLINPAY' or i['payChannel'] == 'WECHAT_WAP_ALLINPAY'):
                wenxin_num  +=  i['num']
                wenxin_total += i['total']
            else:
                print('payChannel is undefined')
                pass

        txt1 = "微信: %s 笔, %s 元" % (wenxin_num,wenxin_total)
        txt2 = "支付宝: %s 笔, %s 元" % (alipay_num,alipay_total)

        data["text"]={"content": "汪汪-(%s)通联朔羡交易汇总: %s 笔, %s 元 \n %s \n %s" % (begin, wenxin_num+alipay_num, wenxin_total+alipay_total, txt1, txt2)}
        print(data)
        #dingding(data)

def zt(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        #中投-支付成功
        sql ='''
            SELECT count(1) num, convert(ifnull(sum(totalFee) / 100, 0), decimal(10, 2)) total
            FROM pay.pay_log_zfzlpay_wechat t1
            WHERE t1.createTime between %s and %s
              AND t1.resultCode = '0000'
        '''
        val = query(db,sql,begin,end)
        txt1 = "支付成功: %s 笔, %s 元" % (val[0],val[1])
        #print(txt1)


        data["text"]={"content": "汪汪-(%s)中投交易汇总\n %s" % (begin,txt1)}
        data["at"]={"atMobiles": ["17301651261"]}
        print(data)
        #write("%s,%s\n" % (i['questTime'],i['amount']))
        #dingding(data)

def union(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        #银联-支付成功
        sql ='''
            SELECT count(1) num, convert(ifnull(sum(amount) / 100, 0), decimal(10, 2)) total
            from acct.acct_paylog_unionpay t1
            where t1.createTime between %s and %s
              and t1.payStatus = 'SUCCESS'
        '''
        val = query(db,sql,begin,end)
        txt1 = "支付成功: %s 笔, %s 元" % (val[0],val[1])
        #print(txt1)


        data["text"]={"content": "汪汪-(%s)银联交易汇总\n %s" % (begin,txt1)}
        #data["at"]={"atMobiles": ["17301651261"]}
        print(data)
        #write("%s,%s\n" % (i['questTime'],i['amount']))
        #dingding(data)

def wex(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        #银联-支付成功
        sql ='''
            SELECT count(1) num, convert(ifnull(sum(total_fee) / 100, 0), decimal(10, 2)) total
            FROM pay.pay_log_wechat t1
            WHERE t1.time_end between %s and %s
                  AND t1.result_code = 'SUCCESS';
        '''
        val = query(db,sql,begin,end)
        txt1 = "支付成功: %s 笔, %s 元" % (val[0],val[1])
        #print(txt1)


        data["text"]={"content": "汪汪-(%s)微信原生交易汇总\n %s" % (begin,txt1)}
        #data["at"]={"atMobiles": ["17301651261"]}
        print(data)
        #write("%s,%s\n" % (i['questTime'],i['amount']))
        #dingding(data)

def ali(begin,end):
    data = {"msgtype": "text"}
    with DB(host='172.16.0.8',user='HxQxaSAPnfjqnJ',passwd='KkZrQWzCeMOeSx',db='acct') as db:
        #银联-支付成功
        sql ='''
            SELECT count(1) num, ifnull(sum(total_fee), 0) total
            FROM pay.pay_log_alipay t1
            WHERE t1.gmt_payment between %s and %s
              AND t1.trade_status = 'TRADE_SUCCESS'
        '''
        val = query(db,sql,begin,end)
        txt1 = "支付成功: %s 笔, %s 元" % (val[0],val[1])
        #print(txt1)


        data["text"]={"content": "汪汪-(%s)支付宝原生交易汇总\n %s" % (begin,txt1)}
        #data["at"]={"atMobiles": ["17301651261"]}
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
    begin = yesterday.strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    wxbegin = yesterday.strftime('%Y%m%d000000')
    wxend = today.strftime('%Y%m%d000000')

    baofu(begin,end)
    tp(begin,end)
    tl(begin,end)
    zt(begin,end)
    union(begin,end)
    wex(wxbegin,wxend)
    ali(begin,end)
