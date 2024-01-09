# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import BaseView, expose


class Setup(BaseView):



    @expose('/')
    def index(self):
        return self.render('admin/setup.html')

