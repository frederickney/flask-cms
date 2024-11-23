# coding: utf-8


from flask import url_for, redirect
from flask_admin import BaseView, expose
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required


class Login(BaseView):

    def __init__(self):
        super(Login, self).__init__(endpoint='admin:login:openid', url='/admin/openid/')
        Process.login_manager().blueprint_login_views.update({'admin:login:openid': "admin:login.index"})

    @expose('/', methods=['GET'])
    def index(self):
        return Process.openid.login(overide_redirect="admin:login:openid")

    @expose('/login/', methods=['GET'])
    def login(self):
        return Process.openid.login(overide_redirect="admin:login:openid")

    @login_required
    @expose('/logout/', methods=['POST', 'GET'])
    def logout(self):
        Process.openid.logout()
        return redirect(url_for('admin'))

    @expose('/authorize/', methods=['POST', 'GET'])
    def authorize(self):
        return Process.openid.authorize()

    def user(self, id):
        return Process.openid.user(id)
