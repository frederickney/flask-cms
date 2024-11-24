# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin.menu import MenuLink


class Logout(MenuLink):

    def __init__(self):
        super(Logout, self).__init__('Logout', endpoint='admin:login.logout')
