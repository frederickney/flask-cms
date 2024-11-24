# coding: utf-8


__author__ = 'Frederick NEY'

from flask import request, redirect, url_for
from flask_framework import Server
from flask_framework.Utils.Auth.ldap import LDAP
from flask_login import LoginManager
from flask_cms import controllers


class Controller(object):
    @classmethod
    @Server.deniedwebcall
    def setup(cls):
        """

        :return:
        """
        Server.Process.login_manager(LoginManager()).init_app(app=Server.Process.get()) \
            if Server.Process.login_manager() is None else Server.Process.login_manager()
        Server.Process.login_manager().blueprint_login_views.update({
            None: 'login'
        })
        Server.Process.login_manager().user_loader(cls.user_loader)
        Server.Process.get().add_url_rule(
            '/ldap/login/', 'ldap.login', controllers.web.login.ldap.index, methods=['GET']
        )
        Server.Process.get().add_url_rule(
            '/ldap/login/', 'ldap.login.send', controllers.web.login.ldap.login, methods=['POST']
        )
        Server.Process.get().add_url_rule(
            '/ldap/logout/', 'ldap.logout', controllers.web.login.ldap.logout, methods=['POST']
        )
        try:
            Server.Process.get().add_url_rule(
                '/logout/', 'logout', controllers.web.login.ldap.logout, methods=['POST']
            )
            Server.Process.get().add_url_rule(
                '/login/', 'login', controllers.web.login.ldap.login, methods=['GET']
            )
            Server.Process.get().add_url_rule(
                '/login/', 'ldap.login.send', controllers.web.login.ldap.login, methods=['POST']
            )
        except Exception as e:
            pass

    @staticmethod
    def index():
        return LDAP.login()

    @staticmethod
    def login():
        return LDAP.login()

    @staticmethod
    def logout():
        return LDAP.logout()

    @staticmethod
    def user_loader(id):
        return LDAP.user_loader(id)

    @classmethod
    def redirect_login(cls):
        return redirect(url_for('ldap.login') + "?next={}".format(request.url))
