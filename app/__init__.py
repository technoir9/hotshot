import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import scrape

def job():
    scrape.run()

def create_app(test_config=None):
    # Configure schedule
    sched = BackgroundScheduler(daemon=True, timezone="Europe/Warsaw")
    # sched.add_job(job, 'interval', hours=12, start_date='2019-08-09 22:00:01')
    sched.add_job(job, 'interval', hours=1, start_date='2019-08-09 18:51:01')
    sched.start()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
