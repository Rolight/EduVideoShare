# -*- coding: utf-8 -*-
#coding=utf-8

# 在蓝本中定义程序路由
from __future__ import print_function

from flask import abort, flash, request
from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user
from sys import stderr

from . import admin
from .forms import EditTagForm, DelTagForm, ManageUserForm
from .. import db
from ..models import User, Tag, Role
from ..decorators import admin_required

# 管理员添加标签
@admin.route('/add_tag', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tag():
    edit_tag_form = EditTagForm()
    edit_tag_form.set_choices()
    if edit_tag_form.validate_on_submit():
        new_tag = Tag(name=edit_tag_form.tagname.data, pre_tag=edit_tag_form.pre_tagname.data)
        db.session.add(new_tag)
        db.session.commit()
        flash(u'标签添加完成')
        print(url_for('admin.add_tag'), file=stderr)
        return redirect(url_for('admin.add_tag'))
    print(repr(request), file=stderr)
    return render_template('/admin/add_tag.html', edit_tag_form=edit_tag_form)

# 管理员删除标签
@admin.route('/del_tag', methods=['GET', 'POST'])
@login_required
@admin_required
def del_tag():
    form = DelTagForm()
    form.set_choices()
    if form.validate_on_submit():
        Tag.query.filter_by(id=form.tagname.data).delete()
        # db.session.commit()
        flash(u'标签删除成功')
        return redirect(url_for('admin.del_tag'))
    return render_template('/admin/del_tag.html', form=form)

# 管理员管理权限
@admin.route('/manage_permission', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_permission():
    form = ManageUserForm()
    form.set_choices()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.username.data).first()
        if user is not None:
            if form.give.data:
                user.role_id = Role.query.filter_by(name=u'Uploader').first().id
            elif form.ungive.data:
                user.role_id = Role.query.filter_by(name=u'User').first().id
            db.session.add(user)
            db.session.commit()
            flash(u'分配权限成功')
        else:
            flash(u'用户不存在')
    return render_template('/admin/manage_permission.html', form=form)




