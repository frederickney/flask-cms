# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import BaseView, expose
from flask_framework.Utils.Auth import admin_login_required as login_required
from flask_framework.Database import Database
from models.persistent import cms
from models import forms


class Settings(BaseView):

    submenu = [
        {'name': 'General', 'endpoint': 'admin:settings.index'},
        {'name': 'Users', 'endpoint': 'admin:settings.users'},
    ]

    def __init__(self):
        super(Settings, self).__init__(endpoint='admin:settings', url='/admin/settings/')

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/setup.html', menu=self.submenu)

    @expose('/general/', methods=['GET'])
    @login_required
    def setting(self):
        return self.render('admin/upload/index.html', form=forms.upload.Form(), menu=self.submenu)

    @expose('/users/', methods=['GET'])
    @login_required
    def users(self):
        users = Database.session.query(cms.Users).all()
        return self.render('admin/users/index.html', menu=self.submenu, users=users)
