# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin import expose
from flask_admin.contrib import rediscli
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required


class RedisCli(rediscli.RedisCli):

    def __init__(self, *args, **kwargs):
        super(RedisCli, self).__init__(*args, **kwargs)
        Process.login_manager().blueprint_login_views.update({'rediscli': "admin:login.index"})

    @login_required
    @expose('/')
    def console_view(self):
        return super(RedisCli, self).console_view()

    @login_required
    @expose('/run/', methods=('POST',))
    def execute_view(self):
        return super(RedisCli, self).execute_view()
