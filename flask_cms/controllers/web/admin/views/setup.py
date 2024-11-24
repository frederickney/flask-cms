# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin import expose

from flask_cms.views import BaseView


class Setup(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/setup.html')
