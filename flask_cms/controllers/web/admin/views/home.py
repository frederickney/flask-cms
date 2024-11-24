# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin import AdminIndexView, expose
from flask_framework.Utils.Auth import admin_login_required as login_required


class Home(AdminIndexView):

    @login_required
    @expose('/')
    def index(self):
        from flask_framework import Extensions
        Extensions.load()
        return self.render('admin/home.html', exts=Extensions.all())
