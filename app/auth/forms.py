# -*- coding: utf-8 -*-
#coding=utf-8

# 为用户提供登录表单

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    username = StringField(u'用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能包含字母数字点号和下划线，并且长度不超过64')])
    password = PasswordField(u'密码', validators=[Required(), Length(6, 18), EqualTo('password2', message=u'密码与确认密码必须相同')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被使用！')
