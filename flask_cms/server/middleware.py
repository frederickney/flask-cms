# coding: utf-8

import logging

from flask import request, current_app
from flask_framework.Config import Environment
from flask_framework.Database import Database
from flask_cms.models.persistent import cms


class Load(object):

    def __init__(self, srv):
        """

        :param srv:
        :type srv: flask.Flask
        """
        srv.before_request(Logger.before)
        srv.before_request(DatabaseLoader.before)
        srv.before_request(ThemeLoader.before)
        srv.after_request(Logger.after)
        srv.after_request(ThemeLoader.after)


class Logger(object):

    @classmethod
    def use(cls):
        """
        :return: call to the decorated function
        """

        def using(func):
            def decorator(*args, **kwargs):
                result = func(*args, **kwargs)
                return result

            return decorator

        return using

    @classmethod
    def after(cls, next=None):
        logging.debug("{}: after request {}".format(__name__, request.path))
        if next is not None:
            return next

    @classmethod
    def before(cls, next=None):
        logging.debug("{}: before request {}".format(__name__, request.path))
        if next is not None:
            return next


class Middlewares(object):

    @classmethod
    def before_request(cls, *args, **kwargs):
        return

    @classmethod
    def after_request(cls, *args, **kwargs):
        return


class ThemeLoader(object):

    theme: str = 'darkly'

    @classmethod
    def use(cls):
        """
        :return: call to the decorated function
        """

        def using(func):
            def decorator(*args, **kwargs):
                result = func(*args, **kwargs)
                return result

            return decorator

        return using

    @classmethod
    def before(cls, next=None):
        theme = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'admin.theme').first()
        current_app.config['FLASK_ADMIN_SWATCH'] = cls.theme if theme is None else theme.setting_value
        return next

    @classmethod
    def after(cls, next=None):
        cls.theme = current_app.config.get('FLASK_ADMIN_SWATCH', cls.theme)
        return next


class DatabaseLoader(object):

    @classmethod
    def reconnect(cls, driver):
        config = Environment.Databases[driver]
        engines_params = {}
        if 'engine' in config:
            engines_params.update(config['engine'])
        Database.register_engine(
            driver,
            config['driver'],
            config['user'],
            config['password'],
            config['address'],
            config['database'],
            port=(config['port'] if 'port' in config else None),
            params=(config['params'] if 'params' in config else None),
            dialects=(config['dialects'] if 'dialects' in config else None),
            echo=Environment.SERVER_DATA['CAPTURE'],
            **engines_params
        )
        if driver == 'default':
            Database.setup(
                config['driver'],
                config['user'],
                config['password'],
                config['address'],
                config['database'],
                port=(config['port'] if 'port' in config else None),
                params=(config['params'] if 'params' in config else None),
                dialects=(config['dialects'] if 'dialects' in config else None),
                echo=Environment.SERVER_DATA['CAPTURE'],
                **engines_params
            )

    @classmethod
    def before(cls):
        for db, connection in Database.engines.items():
            try:
                logging.info("{}: {} is valid {}".format(__name__, db, connection.raw_connection().is_valid))
                if not connection.raw_connection().is_valid:
                    cls.reconnect(db)
            except BrokenPipeError:
                logging.info("{}: {} is valid {}".format(__name__, db, False))
                cls.reconnect(db)
            except Exception:
                logging.info("{}: {} is valid {}".format(__name__, db, False))
                cls.reconnect(db)
            except NotImplemented:
                logging.warning("{}: {} unable to verify connection status".format(__name__, db))
                logging.error("{}: {} unable to reconnect".format(__name__, db))
