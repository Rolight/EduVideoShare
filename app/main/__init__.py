# -*- coding: utf-8 -*-
#coding=utf-8

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

# 把Permission类加入模板上下文
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)