# coding: utf-8


__author__ = 'Frederick NEY'


from flask_login import LoginManager
from flask import Blueprint, current_app
from flask_framework.Config import Environment
import logging
from .login_setup import singlelogin, multilogin


class Login(multilogin.Login if Environment.FLASK['CONFIG'].get('FLASK_CMS_MULTI_LOGIN', False) else singlelogin.Login):

    def __init__(self, lm, adm=None):

        super(Login, self).__init__(lm, adm)

