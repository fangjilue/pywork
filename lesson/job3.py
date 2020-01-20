from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
def aa():
	print("aa")
# BlockingScheduler
scheduler = BlockingScheduler()
#scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
scheduler.add_job(job, 'interval', seconds=5)
scheduler.add_job(aa, 'interval', seconds=3)
scheduler.start()