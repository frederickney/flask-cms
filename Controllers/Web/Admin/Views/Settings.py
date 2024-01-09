# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import BaseView, expose
from flask_login import login_required


class Settings(BaseView):

    submenu = [
        {'name': 'General', 'endpoint': 'admin#settings#index'},
        {'name': 'Users', 'endpoint': 'admin#settings#users'},
    ]

    def __init__(self):
        super(Settings, self).__init__(endpoint='admin#settings', url='/admin/settings/')

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/setup.html', menu=self.submenu)

    @expose('/general/', methods=['GET'])
    @login_required
    def setting(self):
        from Models.Forms.upload import Form
        return self.render('admin/upload/index.html', form=Form(), menu=self.submenu)

    @expose('/users/', methods=['GET'])
    @login_required
    def users(self):
        from Models.Forms.upload import Form
        from flask_framework.Database import Database
        from Models import Persistent
        users = Database.session.query(Persistent.cms.Users).all()
        return self.render('admin/upload/index.html', form=Form(), menu=self.submenu, users = users)
