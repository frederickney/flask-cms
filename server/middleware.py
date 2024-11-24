# coding: utf-8

import flask_cms
from flask_cms.server.middleware import Middlewares


class Load(object):

    def __init__(self, srv):
        """

        :param srv:
        :type srv: flask.Flask
        """
        flask_cms.server.middleware.Load(srv)

