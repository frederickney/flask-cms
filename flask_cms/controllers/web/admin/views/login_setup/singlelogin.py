# coding: utf-8


__author__ = 'Frederick NEY'

from flask import request, redirect, url_for
from flask_admin import BaseView, expose
from flask_framework import Server
from flask_framework.Config import Environment
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_login import current_user

from . import saml, openid, ldap, base


class BaseLogin(BaseView):

    def __init__(self, base_endpoint):
        self.login_endpoint = base_endpoint
        super(BaseLogin, self).__init__(endpoint='admin:login', url='/admin/login/')
        Process.login_manager().blueprint_login_views.update({'admin:login': "admin:login.index"})

    @expose('/', methods=['GET'])
    def index(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin.index'))
        else:
            next = request.args.get('next', None)
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

    def __init__(self, admin=None):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__()
        if Process.login_manager().user_callback is None:
            Process.login_manager().user_loader(self.user)
        Server.Process.get().register_blueprint(BaseLogin(self.endpoint).create_blueprint(admin))
