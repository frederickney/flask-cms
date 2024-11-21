# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask_admin import BaseView, expose
from flask_framework.Config import Environment
from flask_framework.Database import Database
from flask_login import current_user, logout_user
from flask_framework import Server
from flask import request, url_for, redirect, current_app
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_login_oidc import get_client

from . import ldap, base


class Login(BaseView):

    def __init__(self, manager=None, admin=None):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__(endpoint='admin:login', url='/admin/login/')
        manager.init_app(app=Server.Process.get())
        manager.user_loader(self.user)
        manager.unauthorized_handler(self.redirect_login)
        manager.blueprint_login_views = {
            'login': "login",
            'admin': "admin:login.index",
        }
        if current_app.config.get('FLASK_CMS_BASE_ADMIN_LOGIN_TEMPLATE', current_app.get('BASE_LOGIN_TEMPLATE', None)):
            Server.Process.get().register_blueprint(base.Login().create_blueprint(admin))
        #if current_app.config.get('FLASK_CMS_LDAP_ADMIN_LOGIN_TEMPLATE', current_app.get('LDAP_LOGIN_TEMPLATE', None)):
        #    Server.Process.get().register_blueprint(ldap.Login().create_blueprint(admin))

    @expose('/', methods=['GET'])
    def index(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin:index'))
        return self.render(current_app.config.get('FLASK_CMS_MULTI_LOGIN_TEMPLATE'), logins=Environment.Logins)

    @classmethod
    def user(cls, id):
        logging.info("{}: {}".format(__name__, id))
        if type(id) is int:
            if 'BASE' in Environment.Logins:
                from models.persistent import cms
                user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
                return user
            if 'LDAP' in Environment.Logins:
                from models.persistent import cms
                user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
                return user
        if type(id) is str:
            from models.persistent import cms
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

    def redirect_login(self):
        if 'admin' in request.url:
            return redirect(url_for('admin:login.index') + "?next={}".format(request.url))
        else:
            return redirect(url_for('login') + "?next={}".format(request.url))

    @login_required
    @expose('/logout/', methods=['GET', 'POST'])
    def logout(self):
        logout_user()
        return self.render(current_app.config.get('FLASK_CMS_MULTI_LOGIN_TEMPLATE'), logins=Environment.Logins)
