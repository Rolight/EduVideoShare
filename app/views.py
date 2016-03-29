# -*- coding: utf-8 -*-
#coding=utf-8
from app import app

@app.route('/')
@app.route('/index')

def index():
    return "<h1>hello world!</h1>"