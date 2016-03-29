# -*- coding: utf-8 -*-
#coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 如果环境变量中包含钥匙，则使用环境变量中的，否则使用一个默认值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'F*SK!KKCSD(!ds112'
    # 自动提交数据库中的更改
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

# 用户开发环境的配置文件
class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:loulinhui@localhost/eduvideo' + '?charset=utf8'
    ADMINISTRATOR = 'admin'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

# 激活跨站点请求伪造保护
CSRF_ENABLED = True



