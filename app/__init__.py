# -*- coding: utf-8 -*-
#coding=utf-8

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 附加路由定义和错误页面

    #注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

