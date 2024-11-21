# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import BaseView, expose
from flask_framework.Utils.Auth import admin_login_required as login_required


class Appearance(BaseView):

    def __init__(self):
        super(Appearance, self).__init__(endpoint='admin:appearance', url='/admin/appearance/')

    @login_required
    @expose('/')
    def index(self):
        return self.render('admin/setup.html')


