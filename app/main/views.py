# -*- coding: utf-8 -*-
#coding=utf-8

# 在蓝本中定义程序路由
from __future__ import print_function

from flask import abort, flash, request
from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .forms import EditProfileForm
from .. import db
from ..models import User, Tag
from ..decorators import admin_required

from sys import stderr

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
    return render_template('edit_profile.html', form=form)


