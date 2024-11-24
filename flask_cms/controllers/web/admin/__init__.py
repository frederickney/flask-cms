# coding: utf-8


__author__ = 'Frederick NEY'

import logging

import flask_framework.Server as Server
from flask import Flask
from flask_admin import Admin
from flask_framework.Database import Database
from flask_framework.Server import deniedwebcall
from flask_login import LoginManager
from redis import Redis

from flask_cms.models.persistent import cms
from . import ext
from . import menu
from . import views
from .upload import Upload


@deniedwebcall
def setup():
    template = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'admin.template').first()
    adm = Admin(template_mode='bootstrap3' if template is None else template.setting_value, index_view=views.Home())
    app: Flask = Server.Process.get()
    theme = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'admin.theme').first()
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly' if theme is None else theme.setting_value
    adm.init_app(app)
    Server.Process._admin = adm
    Server.Process.login_manager(LoginManager()).init_app(app=Server.Process.get()) \
        if Server.Process.login_manager() is None else Server.Process.login_manager()
    load_views(adm, app, Server.Process.login_manager())


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
        logging.info("{}: Create LoginManager in {}".format(__name__, __file__))
        login_manager = LoginManager()
        login_manager.init_app(Server.Process.get())
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
    app.register_blueprint(views.Login(adm).create_blueprint(adm))
    if 'redis' in Environment.Services:
        adm.add_views(
            views.RedisCli(Redis(Environment.Services['redis']['HOST'], Environment.Services['redis']['PORT'])))
