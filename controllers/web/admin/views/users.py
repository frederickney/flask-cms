# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import BaseView, expose
from flask_framework.Utils.Auth import admin_login_required as login_required


class Users(BaseView):

    def __init__(self):
        super(Users, self).__init__()

    @login_required
    @expose('/')
    def index(self):
        return self.render('admin/setup.html')


