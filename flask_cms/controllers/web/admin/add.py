# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin.menu import MenuLink


class Add(MenuLink):

    def __init__(self, parent):
        super(Add, self).__init__(
            "Add",
            endpoint='admin:%s:add' % parent.split('.')[-1].lower(),
            category=parent.split('.')[-1]
        )
