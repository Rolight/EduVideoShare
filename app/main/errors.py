# -*- coding: utf-8 -*-
#coding=utf-8

from flask import render_template
from . import main

# 这里要注意的是，如果使用errorhandler修饰器，那么只有蓝本中的错误才能出发处理程序。
# 要想注册全局的错误处理程序，必须使用app_errorhandler
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

