# coding: utf-8
import logging

from flask_admin import BaseView, expose
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_framework.Utils.Auth.ldap import LDAP
from flask_framework.Database import Database
from flask import flash, redirect, url_for, request, current_app
import os


class Login(BaseView):

    def __init__(self):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__(endpoint='admin:login:ldap', url='/admin/ldap/')

    @expose('/', methods=['GET'])
    def index(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin'))
        else:
            next = request.args.get('next', None)
            if next:
                return redirect(url_for('admin:login:ldap.login'))
            return redirect(url_for('admin:login:ldap.login'))

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin'))
        return LDAP.login(
            current_app.config.get('FLASK_CMS_LDAP_ADMIN_LOGIN_TEMPLATE', current_app.config["LDAP_LOGIN_TEMPLATE"])
        )

    @staticmethod
    def user(id):
        logging.info("{}: {}".format(__name__, id))
        from models.persistent import cms
        user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
        return user

    @expose('/logout/', methods=['POST'])
    @login_required
    def logout(cls):
        return LDAP.logout('admin:login.index')

    @staticmethod
    def redirect_login():
        return redirect(url_for('admin:login:ldap.index') +"?next={}".format(request.url))
