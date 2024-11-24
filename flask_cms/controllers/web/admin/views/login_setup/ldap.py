# coding: utf-8

from flask import redirect, url_for, request, current_app
from flask_admin import expose
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_framework.Utils.Auth.ldap import LDAP
from flask_login import current_user

from flask_cms.models.persistent import cms
from flask_cms.views import BaseView

class Login(BaseView):

    def __init__(self):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__(endpoint='admin:login:ldap', url='/admin/ldap/')
        Process.login_manager().blueprint_login_views.update({'admin:login:ldap': "admin:login.index"})

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
        user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
        return user

    @expose('/logout/', methods=['POST', 'GET'])
    @login_required
    def logout(cls):
        return LDAP.logout('admin:login.index')
