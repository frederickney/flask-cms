# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin import BaseView, expose
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models.persistent import cms


class Users(BaseView):
    submenu = [
        {'name': 'General', 'endpoint': 'admin:settings.setting'},
        {'name': 'Users', 'endpoint': 'admin:settings:users.all'},
    ]

    def __init__(self):
        super(Users, self).__init__(endpoint='admin:settings:users', url='/admin/settings/users/')
        Process.login_manager().blueprint_login_views.update({'admin:settings:users': "admin:login.index"})

    @expose('/')
    @login_required
    def all(self):
        users = Database.session.query(cms.Users).all()
        return self.render('admin/users/index.html', menu=self.submenu, users=users)

    @expose('/<user_id>/')
    @login_required
    def index(self, user_id):
        users = Database.session.query(cms.Users).filter(cms.Users.id == user_id).all()
        return self.render('admin/users/index.html', menu=self.submenu, users=users)
