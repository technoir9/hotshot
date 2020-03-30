import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from . import scrape

def job():
    scrape.run()

def init_scheduler():
    sched = BackgroundScheduler(daemon=True, timezone="Europe/Warsaw")
    sched.add_job(job, 'interval', hours=12, start_date='2019-08-10 10:00:05')
    sched.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: sched.shutdown())
