# coding: utf-8

__author__ = 'Frédérick NEY'

import logging

from flask import request
from flask import render_template as template

from flask_cms.models.persistent import cms
from flask_framework.Controllers.Web.HTTP40XController import page_or_error404
from flask_framework.Database import Database
from flask_login import current_user


class Controller(object):

    @staticmethod
    def index():
        return

    @staticmethod
    def render_or_not_found(error):
        logging.info(request.path)
        content = Database.session.query(cms.Contents).filter(cms.Contents.url == request.path).first()
        theme = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'site.theme').first()
        theme = 'default' if theme is None else theme.setting_value
        logging.info("{}: Loaded theme {}".format(__name__, theme))
        if content:
            if hasattr(current_user, 'is_admin'):
                if current_user.is_admin:
                    return template(
                        "themes/{}/{}.html".format(theme, content.type),
                        page=content,
                        bd=Database.session,
                        theme=theme
                    )
            if content.activated:
                return template(
                    "themes/{}/{}.html".format(theme, content.type),
                    page=content,
                    bd=Database.session,
                    theme=theme
                )
        return page_or_error404(error)

