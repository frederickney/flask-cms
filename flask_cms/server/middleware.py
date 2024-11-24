# coding: utf-8

import logging

from flask import request


class Load(object):

    def __init__(self, srv):
        """

        :param srv:
        :type srv: flask.Flask
        """
        srv.before_request(Logger.before)
        srv.after_request(Logger.after)


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
