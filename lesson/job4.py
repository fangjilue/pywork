from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# BlockingScheduler
scheduler = BackgroundScheduler()

# 输出时间
@scheduler.scheduled_job('cron', id='my_job_id', hour=17,minute=0,second=0)
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def aa():
	print("aa")

#scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)

scheduler.add_job(aa, 'cron', day=1, hour=0, minute=0,second=0)
scheduler.start()