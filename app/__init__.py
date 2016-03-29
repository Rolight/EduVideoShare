# -*- coding: utf-8 -*-
#coding=utf-8

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

# Bootstrap 模板
bootstrap = Bootstrap()

# 处理时间
moment = Moment()

# 处理数据库
db = SQLAlchemy()

# 登录页面管理器
login_manager = LoginManager()
login_manager.session_protection = 'strong'  #安全级别高
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 附加路由定义和错误页面

    #注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app

