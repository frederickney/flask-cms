# coding: utf-8


__author__ = 'Frederick NEY'

from flask_framework.Config import Environment
from flask_framework.Server import Process

from .login_setup import singlelogin, multilogin


class Login(multilogin.Login if Environment.FLASK['CONFIG'].get('FLASK_CMS_MULTI_LOGIN', False) else singlelogin.Login):

    def __init__(self, adm=None):
        super(Login, self).__init__(adm)
        Process.login_manager().blueprint_login_views.update({'admin': 'admin:login.index'})
