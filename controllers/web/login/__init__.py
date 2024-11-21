# coding: utf-8


__author__ = 'Frederick NEY'


import logging
from flask import url_for, request, redirect, flash
from flask import render_template as template
from flask_login import logout_user, LoginManager
from flask_framework import Server
from flask_framework.Database import Database
from models.persistent import cms
from flask_framework.Config import Environment
from json import JSONDecodeError



try:
    from .ldap import Controller as ldap
except AttributeError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
except ImportError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass

try:
    from .saml import Controller as saml
except AttributeError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
except ImportError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass

"""
try:
    from .sso import Controller as sso
except AttributeError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
except ImportError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
"""


try:
    from .openid import Controller as openid
except AttributeError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
except ImportError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass


try:
    from .local import Controller as local
except AttributeError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
except ImportError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass


class Manage():

    @classmethod
    def setup(cls):
        Server.Process._manager = LoginManager()
        Server.Process._manager.init_app(app=Server.Process.get())
        Server.Process._manager.unauthorized_handler(cls.redirect_login)
        Server.Process._manager.user_loader(cls.user_loader)
        pass

    @classmethod
    def login(cls):
        return template('login/index.html', logins=Environment.Logins, theme='default')


    @classmethod
    def logout(cls):
        """
        flask logout view
        :return:
        """
        logout_user()
        flash('logged out')
        return redirect(url_for('login'))

    @classmethod
    def redirect_login(cls):
        return redirect(url_for('login') + "?next={}".format(request.url))

    @staticmethod
    def user_loader(id):
        logging.info("{}: {}".format(__name__, id))
        if type(id) is int:
            if 'BASE' in Environment.Logins:
                from models.persistent import cms
                user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
                return user
            if 'LDAP' in Environment.Logins:
                from models.persistent import cms
                user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
                return user
        if type(id) is str:
            from models.persistent import cms
            user = None
            try:
                from flask_login_oidc import get_client
                user = cms.Users.load_from_token(get_client('OPENID'), id)
            except KeyError:
                pass
            except JSONDecodeError:
                pass
            try:
                user = cms.Users.load_from_assertion(id)
            except KeyError:
                pass
            return user
        if type(id) == dict:
            from models.persistent import cms
            user = None
            try:
                from flask_login_oidc import get_client
                user = cms.Users.load_from_token(get_client('OPENID'), id)
            except KeyError:
                pass
            return user
        return None
