# -*- coding: utf-8 -*-
#coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from . import db
# 使用werkzeug库进行密码散列
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from . import login_manager

# 用户权限代码
class Permission:
    # 上传视频
    UPLOAD_VIDEO = 0x01
    # 编辑标签
    EDIT_TAG = 0x02
    # 分配权限
    LIKE_ADMIN = 0x04

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    # 往数据库中添加角色
    @staticmethod
    def insert_roles():
        # 一共三种角色，视频上传者，管理员和普通用户
        roles = {
            'User': (0, True),
            'Uploader': (Permission.UPLOAD_VIDEO, False),
            'Admin': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['ADMINISTRATOR']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # property装饰器用于将一个成员方法变成属性，之后就可以利用setter和getter修饰器方便进行检查
    @property
    def password(self):
        raise AttributeError(u'密码不是一个可读属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @password.setter
    def __repr__(self):
        return '<User %r>' % self.username

    # 判断是否有权限
    def can(self, permissions):
       return self.role is not None and (self.role.permissions & permissions) == permissions

    # 判断是否是超级管理员
    def is_administrator(self):
        return self.can(Permission.LIKE_ADMIN)

# 匿名用户
class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

# flask.login必要的回调函数
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 视频标签关系表
videotags = db.Table('videotags',
                     db.Column('video_id', db.Integer, db.ForeignKey('videos.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )

# 标签关系表
class TagRelation(db.Model):
    __tablename__ = 'tagrs'
    # 标签编号
    id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, index=True)
    # 子标签编号
    child_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, index=True)


# 标签表
class Tag(db.Model):
    __tablename__ = 'tags'
    # 标签编号
    id = db.Column(db.Integer, primary_key=True)
    # 标签名称
    name = db.Column(db.String(64))
    # 子标签
    sub_tags = db.relationship('TagRelation', foreign_keys=[TagRelation.child_id],
                               backref=db.backref('pre_tags', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    # 父标签
    pre_tags = db.relationship('TagRelation', foreign_keys=[TagRelation.id],
                               backref=db.backref('sub_tags', lazy='joined'),
                               cascade='all, delete-orphan')
    #添加默认标签
    @staticmethod
    def add_empty_tag():
        tag = Tag.query.filter_by(id=1).first()
        if tag is None:
            tag = Tag(name=u'无', id=1)
            db.session.add(tag)
            db.session.commit()



# 视频信息表
class Video(db.Model):
    __tablename__ = 'videos'
    # 视频编号
    id = db.Column(db.Integer, primary_key=True)
    # 视频上传者
    uploader = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 视频名称
    name = db.Column(db.String(128), nullable=False)
    # 上传日期
    upload_date = db.Column(db.Date, nullable=False)
    # 文件路径
    path = db.Column(db.String(512), nullable=False)
    # 视频标签
    tags = db.relationship('Tag',
                           secondary=videotags,
                           backref=db.backref('videos', lazy='dynamic'),
                           lazy='dynamic')


