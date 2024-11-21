# coding: utf-8
import logging

from flask_login import LoginManager
from flask_framework.Config import Environment

__author__ = 'Frederick NEY'


class Route(object):
    """
    Class that will configure all web based routes for the server
    """

    def __init__(self, server):
        """
        Constructor
        :param server: Flask server
        :type server: flask.Flask
        :return: Route object
        """
        import controllers
        server.add_url_rule('/', "home", controllers.web.home.default, methods=["GET"])
        server.add_url_rule('/test', "test", controllers.web.home.test, methods=["GET"])
        if Environment.Logins:
            if len(Environment.Logins) > 1:
                logging.info("{}: Loading loging routes for multi login site")
                server.add_url_rule('/logout/', "logout", controllers.web.login.Manage.logout, methods=["GET", "POST"])
                server.add_url_rule('/login/', "login", controllers.web.login.Manage.login, methods=["GET"])
            if 'BASE' in Environment.Logins:
                controllers.web.login.local.setup()
            if 'LDAP' in Environment.Logins:
                controllers.web.login.ldap.setup()
            if 'OpenID' in Environment.Logins:
                controllers.web.login.openid.setup()
            if 'SAML2' in Environment.Logins:
                controllers.web.login.saml.setup()
        if len(Environment.Logins) > 1:
            logging.info("{}: Loading loging manager for multi login site")
            controllers.web.login.Manage.setup()
        controllers.web.admin.setup()
        #server.add_url_rule('/sso', 'sso', controllers.web.login.sso.login_callback, ['GET'])
        return

