import os
import atexit
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from utils import scrape

sched = BackgroundScheduler(daemon=True, timezone="Europe/Warsaw")

def job():
    print('job')
    scrape.run(os.environ['TEMP_WEBHOOK'])

def init_scheduler():
    print('init_scheduler')
    sched.add_job(job, 'interval', hours=12, start_date='2019-08-10 11:00:05')
    sched.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: sched.shutdown())

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

@app.route('/hotshot_run')
def hotshot_run():
    print('hotshot_run')
    # if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    if not sched.running:
        print('sched not running')
        init_scheduler()
    return 'Schedule initialized'

if __name__ == '__main__':
    print('__name__ == __main__')
    app.run(use_reloader=False)

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     return app
