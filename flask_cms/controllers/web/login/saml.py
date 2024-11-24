# coding: utf-8


__author__ = 'Frederick NEY'

import flask
from flask_framework import Server
from flask_login import login_required, LoginManager
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
            '/saml2/login/', 'saml2.login', controllers.web.login.saml.index, methods=['GET']
        )
        Server.Process.get().add_url_rule(
            '/saml2/authorize/', 'saml2.authorize', controllers.web.login.saml.login, methods=['POST']
        )
        Server.Process.get().add_url_rule(
            '/saml2/metadata/', 'saml2.metadata', controllers.web.login.saml.metadata, methods=['GET']
        )
        Server.Process.get().add_url_rule(
            '/saml2/logout/', 'saml2.logout', controllers.web.login.saml.logout, methods=['POST']
        )
        Server.Process._csrf.exempt("{}.login".format(__name__))
        Server.Process._csrf.exempt("{}.logout".format(__name__))
        try:
            Server.Process.get().add_url_rule(
                '/logout/', 'logout', controllers.web.login.saml.logout, methods=['GET']
            )
            Server.Process.get().add_url_rule(
                '/login/', 'login', controllers.web.login.saml.index, methods=['GET']
            )
            Server.Process.get().add_url_rule(
                '/authorize/', 'authorize', controllers.web.login.saml.login, methods=['POST']
            )
        except Exception as e:
            pass

    @staticmethod
    def redirect_login():
        return flask.redirect(flask.url_for('saml.login'))

    @staticmethod
    def index():
        return Server.Process.saml.saml_login()

    @staticmethod
    def metadata():
        return Server.Process.saml.metadata()

    @staticmethod
    def login():
        return Server.Process.saml.authorize()

    @staticmethod
    @login_required
    def logout():
        return Server.Process.saml.saml_logout()

    @staticmethod
    def user_loader(id):
        return Server.Process.openid.user(id)
