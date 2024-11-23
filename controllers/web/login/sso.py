# coding: utf-8


__author__ = 'Frederick NEY'

from flask import session
from flask_framework.Server import Process


class Controller(object):
    @staticmethod
    @Process.sso.login_handler
    def login_callback(user_info):
        """Store information in session."""
        print(user_info)
        session['user'] = user_info
