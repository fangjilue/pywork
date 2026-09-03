#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import redis
from apscheduler.schedulers.blocking import BlockingScheduler

def myjob():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    key = 'Pms:yuxiaor:d0channel:enabled:company:tailno'
    num =r.scard(key)
    if num > 9:
        return
    r.sadd(key,num)
    print(r.smembers(key))
    print(r.sismember(key,num))
    print(r.scard(key))

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(myjob, 'cron', hour=0, minute=1,second=0)
    scheduler.start()