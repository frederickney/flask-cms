# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask_admin import expose
from flask_admin.contrib import rediscli
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required


class RedisCli(rediscli.RedisCli):

    def __init__(self, redis, static_folder, template_folder, *args, **kwargs):
        logging.info("{}: {} {}".format(__name__, static_folder, template_folder))
        super(RedisCli, self).__init__(redis, *args, **kwargs)
        self.static_folder = static_folder
        self.template_folder = template_folder
        Process.login_manager().blueprint_login_views.update({'rediscli': "admin:login.index"})

    @login_required
    @expose('/')
    def console_view(self):
        return self.render('admin/rediscli/client.html')

    @login_required
    @expose('/run/', methods=['POST'])
    def execute_view(self):
        return super(RedisCli, self).execute_view()

    def create_blueprint(self, admin):
        bp = super(RedisCli, self).create_blueprint(admin)
        bp.template_folder = self.template_folder
        logging.info(self.template_folder)
        return bp