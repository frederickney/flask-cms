# coding: utf-8


__author__ = 'Frederick NEY'


from flask import g, session, jsonify, request
import flask
import logging
from flask import redirect, url_for
from flask_login import LoginManager, login_required
from flask_framework.Server import Process


class Controller(object):

    @classmethod
    def setup(cls):
        from flask_framework import Server
        import controllers
        Server.Process._manager = LoginManager()
        Server.Process._manager.init_app(app=Server.Process.get())
        Server.Process._manager.unauthorized_handler(cls.redirect_login)
        Server.Process._manager.user_loader(cls.user_loader)
        Server.Process.get().add_url_rule('/openid/login/', 'openid.login', controllers.web.login.openid.index, methods=['GET'])
        Server.Process.get().add_url_rule('/openid/authorize/', 'openid.authorize', controllers.web.login.openid.login, methods=['GET'])
        Server.Process.get().add_url_rule('/openid/logout/', 'openid.logout', controllers.web.login.openid.logout, methods=['POST'])
        try:
            Server.Process.get().add_url_rule('/logout/', 'logout', controllers.web.login.openid.logout, methods=['GET'])
            Server.Process.get().add_url_rule('/login/', 'login', controllers.web.login.openid.index, methods=['GET'])
            Server.Process.get().add_url_rule('/authorize/', 'authorize', controllers.web.login.openid.login, methods=['POST'])
        except Exception as e:
            pass

    @staticmethod
    def index():
        next = request.args.get('next')
        return Process.openid.login()

    @staticmethod
    @login_required
    def logout():
        Process.openid.logout()
        return redirect(url_for('home'))

    @staticmethod
    def login():
        return Process.openid.authorize()

    @staticmethod
    def user_loader(id):
        return Process.openid.user(id)

    @classmethod
    def redirect_login(cls):
        return redirect(url_for('openid.login') + "?next={}".format(request.url))
