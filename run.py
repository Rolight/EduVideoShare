# -*- coding: utf-8 -*-
#coding=utf-8

#!flask/bin/python

import os
from app import create_app, db
from app.models import User, Role, Tag, TagRelation, Video, videotags
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

migrate = Migrate(app, db)

# 在shell模式下自动加载数据库
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Tag=Tag, TagRelation=TagRelation, Video=Video, videotags=videotags)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
