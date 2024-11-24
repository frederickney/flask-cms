# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask import url_for, redirect, current_app
from flask_admin import BaseView, expose
from flask_framework import Server
from flask_framework.Config import Environment
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_login import current_user, logout_user
from flask_login_oidc import get_client

from flask_cms.models.persistent import cms
from . import base
from . import ldap
from . import openid
from . import saml


class Login(BaseView):
    _enabled_logins = []

    def __init__(self, admin=None):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__(endpoint='admin:login', url='/admin/login/')
        Process.login_manager().blueprint_login_views.update({'admin:login': "admin:login.index"})

        if (Server.Process.get().config.get(
                'FLASK_CMS_BASE_ADMIN_LOGIN_TEMPLATE',
                Server.Process.get().config.get('BASE_LOGIN_TEMPLATE', None)
        )):
            Server.Process.get().register_blueprint(base.Login().create_blueprint(admin))
            self._enabled_logins.append('admin:login:base')
        if (Server.Process.get().config.get(
                'FLASK_CMS_LDAP_ADMIN_LOGIN_TEMPLATE',
                Server.Process.get().config.get('LDAP_LOGIN_TEMPLATE', None)
        )):
            Server.Process.get().register_blueprint(ldap.Login().create_blueprint(admin))
            self._enabled_logins.append('admin:login:ldap')
        if Server.Process.openid is not None:
            Server.Process.get().register_blueprint(openid.Login().create_blueprint(admin))
            self._enabled_logins.append('admin:login:openid')
        if Server.Process.saml is not None:
            Server.Process.get().register_blueprint(saml.Login().create_blueprint(admin))
            self._enabled_logins.append('admin:login:saml2')

    @expose('/', methods=['GET'])
    def index(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin:index'))
        return self.render(current_app.config.get('FLASK_CMS_MULTI_LOGIN_TEMPLATE'), logins=self._enabled_logins)

    @classmethod
    def user(cls, id):
        if type(id) is int:
            if 'BASE' in Environment.Logins:
                user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
                return user
            if 'LDAP' in Environment.Logins:
                user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
                return user
        if type(id) is str:
            user = None
            try:
                user = cms.Users.load_from_token(get_client('OPENID'), id)
            except KeyError:
                pass
            try:
                user = cms.Users.load_from_assertion(id)
            except KeyError:
                pass
            return user
        return None

    @login_required
    @expose('/logout/', methods=['GET', 'POST'])
    def logout(self):
        logout_user()
        return self.render(current_app.config.get('FLASK_CMS_MULTI_LOGIN_TEMPLATE'), logins=Environment.Logins)
