# coding: utf-8


__author__ = 'Frederick NEY'

import flask
from flask import session
from flask_login import login_required, LoginManager
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
        Server.Process.get().add_url_rule('/saml2/login/', 'saml2.login', controllers.web.login.saml.index, methods=['GET'])
        Server.Process.get().add_url_rule('/saml2/authorize/', 'saml2.authorize', controllers.web.login.saml.login, methods=['POST'])
        Server.Process.get().add_url_rule('/saml2/metadata/', 'saml2.metadata', controllers.web.login.saml.login, methods=['GET'])
        Server.Process.get().add_url_rule('/saml2/logout/', 'saml2.logout', controllers.web.login.saml.logout, methods=['POST'])
        Process._csrf.exempt("{}.login".format(__name__))
        Process._csrf.exempt("{}.logout".format(__name__))
        try:
            Server.Process.get().add_url_rule('/logout/', 'logout', controllers.web.login.saml.logout, methods=['GET'])
            Server.Process.get().add_url_rule('/login/', 'login', controllers.web.login.saml.index, methods=['GET'])
            Server.Process.get().add_url_rule('/authorize/', 'authorize', controllers.web.login.saml.login, methods=['POST'])
        except Exception as e:
            pass

    @staticmethod
    def redirect_login():
        return flask.redirect(flask.url_for('saml.login'))

    @staticmethod
    def index():
        return Process.saml.saml_login()

    @staticmethod
    def metadata():
        return Process.saml.metadata()

    @staticmethod
    def login():
        return Process.saml.authorize()

    @staticmethod
    @login_required
    def logout():
        return Process.saml.saml_logout()

    @staticmethod
    def user_loader(id):
        return Process.openid.user(id)