# -*- coding: utf-8 -*-
#coding=utf-8

# 在蓝本中定义程序路由

from flask import abort, flash
from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .forms import EditProfileForm, EditTagForm
from .. import db
from ..models import User
from ..decorators import admin_required

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.password_
    return render_template('edit_profile.html', form=form)

# 管理员页面，可以添加修改标签，赋予上传权限
@main.route('/admin-edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit():
    edit_tag_form = EditTagForm()
    return render_template('admin_edit.html', edit_tag_form=edit_tag_form)

