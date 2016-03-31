# -*- coding: utf-8 -*-
#coding=utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

# 用户资料编辑器，用来修改密码
class EditProfileForm(Form):
    password = PasswordField(u'密码', validators=[Required(), Length(6, 18), EqualTo('password2', message=u'密码与确认密码必须相同')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'保存修改')

# 标签编辑器，用来编辑视频标签
class EditTagForm(Form):
    pre_tagname = SelectField(u'上级标签', choices=[('a', 'aa'), ('b', 'bb')])
    tagname = StringField(u'标签名称', validators=[Required()])
    save = SubmitField(u'添加标签')
    
