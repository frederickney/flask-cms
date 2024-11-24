# coding: utf-8


__author__ = 'Frederick NEY'

from flask import redirect, url_for
from flask import request
from flask_framework import Server
from flask_login import LoginManager, login_required
from flask_cms import controllers


class Controller(object):

    @classmethod
    def setup(cls):
        Server.Process.login_manager(LoginManager()).init_app(app=Server.Process.get()) \
            if Server.Process.login_manager() is None else Server.Process.login_manager()
        Server.Process.login_manager().blueprint_login_views.update({
            None: 'login'
        })
        Server.Process.login_manager().user_loader(cls.user_loader)
        Server.Process.get().add_url_rule(
            '/openid/login/', 'openid.login', controllers.web.login.openid.index, methods=['GET']
        )
        Server.Process.get().add_url_rule(
            '/openid/authorize/', 'openid.authorize', controllers.web.login.openid.login, methods=['GET']
        )
        Server.Process.get().add_url_rule(
            '/openid/logout/', 'openid.logout', controllers.web.login.openid.logout, methods=['POST']
        )
        try:
            Server.Process.get().add_url_rule(
                '/logout/', 'logout', controllers.web.login.openid.logout, methods=['GET']
            )
            Server.Process.get().add_url_rule(
                '/login/', 'login', controllers.web.login.openid.index, methods=['GET']
            )
            Server.Process.get().add_url_rule(
                '/authorize/', 'authorize', controllers.web.login.openid.login, methods=['POST']
            )
        except Exception as e:
            pass

    @staticmethod
    def index():
        next = request.args.get('next')
        return Server.Process.openid.login()

    @staticmethod
    @login_required
    def logout():
        Server.Process.openid.logout()
        return redirect(url_for('home'))

    @staticmethod
    def login():
        return Server.Process.openid.authorize()

    @staticmethod
    def user_loader(id):
        return Server.Process.openid.user(id)

    @classmethod
    def redirect_login(cls):
        return redirect(url_for('openid.login') + "?next={}".format(request.url))
