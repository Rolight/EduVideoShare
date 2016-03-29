# -*- coding: utf-8 -*-
#coding=utf-8

# 在蓝本中定义程序路由

from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    return 'this is index page'
