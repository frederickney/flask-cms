# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from . import ext
from .upload import Upload
from flask_framework.Server import deniedwebcall
from flask_admin.contrib import rediscli
from flask_login import LoginManager
from redis import Redis
from flask import Flask
from . import menu
from . import views
import flask_framework.Server as Server
from flask_admin import Admin


@deniedwebcall
def setup():
    adm = Admin(template_mode='bootstrap3', index_view=views.Home())
    app: Flask = Server.Process.get()
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    adm.init_app(app)
    Server.Process._admin = adm
    load_views(adm, app, getattr(Server.Process, '_manager', Server.Process._manager))


@deniedwebcall
def load_views(adm, app, login_manager=None):
    from flask_framework.Config import Environment
    """

    :param adm:
    :type adm: flask_admin.Admin
    :param app:
    :type app: flask.Flask
    :return:
    """
    if not login_manager:
        logging.warning("{}: Create LoginManager in {}".format(__name__, __file__))
        login_manager = LoginManager()
    if login_manager:
        if login_manager.unauthorized_callback:
            login_manager.unauthorized_handler(None)
    adm.add_link(menu.links.Site())
    adm.add_link(menu.links.Logout())
    adm.add_view(views.Plugins())
    adm.add_view(views.Pages())
    adm.add_view(views.Medias())
    adm.add_view(views.Appearance())
    adm.add_view(views.Settings())
    adm.add_sub_category('Users', 'Settings')
    app.register_blueprint(views.Users().create_blueprint(adm))
    app.register_blueprint(views.Login(login_manager, adm).create_blueprint(adm))
    if 'redis' in Environment.Services:
        adm.add_views(rediscli.RedisCli(Redis(Environment.Services['redis']['HOST'], Environment.Services['redis']['PORT'])))
