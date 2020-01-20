#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from selector.autoquery import myjob
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    scheduler = BackgroundScheduler()
    #scheduler.add_job(myjob, 'cron', day=1, hour=0, minute=0,second=0)
    #scheduler.add_job(myjob, 'cron', hour=17,minute=0,second=0)
    scheduler.add_job(myjob, 'interval', seconds=5)
    scheduler.start()
    return app
