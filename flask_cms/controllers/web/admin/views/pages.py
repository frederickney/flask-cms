# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin import expose
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models import forms
from flask_cms.views import BaseView


class Pages(BaseView):

    def __init__(self):
        super(Pages, self).__init__(endpoint='admin:pages', url='/admin/pages/')
        Process.login_manager().blueprint_login_views.update({'admin:pages': "admin:login.index"})

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/setup.html')

    @expose('/add/', methods=['GET'])
    @login_required
    def add(self):
        return self.render('admin/upload/index.html', form=forms.upload.Content())

    @expose('/save/', methods=['POST'])
    @login_required
    def save(self):
        pass

    @expose('/delete/', methods=['POST'])
    @login_required
    def delete(self):
        pass
