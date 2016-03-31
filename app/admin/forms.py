# -*- coding: utf-8 -*-
#coding=utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Tag

# 标签编辑器，用来编辑视频标签
class EditTagForm(Form):
    pre_tagname = SelectField(u'上级标签', choices=[], coerce=int)
    tagname = StringField(u'标签名称', validators=[Required()])
    save = SubmitField(u'添加标签')

    def set_choices(self):
        choices = []
        for tag in Tag.query.all():
            nowtag = tag
            now_path = tag.name
            while nowtag.id != 1:
                nowtag = nowtag.get_pre_tag()
                if nowtag.id == 1:
                    break
                now_path = nowtag.name + '->' + now_path
            choices.append((tag.id, now_path))
        self.pre_tagname.choices = choices

# 删除标签
class DelTagForm(Form):
    tagname = SelectField(u'标签名称', coerce=int)
    save = SubmitField(u'删除标签')

    def set_choices(self):
        choices = []
        for tag in Tag.query.all():
            nowtag = tag
            now_path = tag.name
            while nowtag.id != 1:
                nowtag = nowtag.get_pre_tag()
                if nowtag.id == 1:
                    break
                now_path = nowtag.name + '->' + now_path
            choices.append((tag.id, now_path))
        self.tagname.choices = choices

# 分配权限
class ManageUserForm(Form):
    username = SelectField(u'用户名', coerce=int)
    give = SubmitField(u'给与上传权限')
    ungive = SubmitField(u'收回上传权限')

    def set_choices(self):
        self.username.choices = [(x.id, x.username) for x in User.query.all()]



