# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask_framework.Config import Environment
from Crypto.Hash import SHA512

from flask_admin import BaseView, expose
from flask_framework import Server
from flask_framework.Database import Database
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_login import current_user
from flask_login import login_user, logout_user
from flask import request, redirect, url_for, flash, Blueprint
from . import saml, openid, ldap, base

from models import forms
from models.persistent import cms


class BaseLogin(BaseView):

    def __init__(self, base_endpoint):
        self.login_endpoint = base_endpoint
        super(BaseLogin, self).__init__(endpoint='admin:login', url='/admin/login/')

    @expose('/', methods=['GET'])
    def index(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin'))
        else:
            next = request.args.get('next', None)
            logging.info(url_for("{}.index".format(self.login_endpoint)))
            if next:
                return redirect(url_for("{}.index".format(self.login_endpoint)) + "?next={}".format(next))
            return redirect(url_for("{}.index".format(self.login_endpoint)))

    @expose('/logout/', methods=['POST', 'GET'])
    @login_required
    def logout(self):
        return redirect(url_for("{}.logout".format(self.login_endpoint)))


class Login(
    openid.Login if Environment.FLASK['CONFIG'].get('FLASK_CMS_BASE_LOGIN', 'BASE') == 'OpenID' else
    saml.Login if Environment.FLASK['CONFIG'].get('FLASK_CMS_BASE_LOGIN', 'BASE') == 'SAML2' else
    ldap.Login if Environment.FLASK['CONFIG'].get('FLASK_CMS_BASE_LOGIN', 'BASE') == 'LDAP' else
    base.Login
):

    def __init__(self, manager=None, admin=None):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__()
        manager.init_app(app=Server.Process.get())
        if manager.user_callback == None:
            manager.user_loader(self.user)
            #manager.unauthorized_handler(self.redirect_login)

        Server.Process.get().register_blueprint(BaseLogin(self.endpoint).create_blueprint(admin))
        manager.blueprint_login_views.update(
            {
                None: "login",
                'admin': "admin:login.index",
                'admin:medias': "admin:login.index",
                'admin:pages': "admin:login.index",
                'admin:plugins': "admin:login.index",
                'admin:settings': "admin:login.index",
                'admin:appearance': "admin:login.index",
                'users': "admin:login.index",
            }
        )
        self.manager = manager

    def redirect_login(self):
        if 'admin' in request.url:
            return redirect(url_for('admin:login.index') + "?next={}".format(request.url))
        else:
            return redirect(url_for('login') + "?next={}".format(request.url))
