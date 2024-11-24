# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import os

import flask_admin
from flask import request, redirect, Flask
from flask_admin import expose
from flask_framework.Config import Environment
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models import forms
from flask_cms.models.persistent import cms
from flask_cms.views import BaseView


class Appearance(BaseView):
    submenu = [
        {'name': 'Website', 'endpoint': 'admin:appearance.site'},
        {'name': 'Admin panel', 'endpoint': 'admin:appearance.panel'},
    ]

    def __init__(self):
        super(Appearance, self).__init__(endpoint='admin:appearance', url='/admin/appearance/')
        Process.login_manager().blueprint_login_views.update({'admin:appearance': "admin:login.index"})

    @expose('/', methods=['GET'])
    @login_required
    def index(self):
        return self.render('admin/setup.html', menu=self.submenu)

    @login_required
    @expose('/admin/', methods=['GET', 'POST'])
    def panel(self):
        template = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'admin.template').first()
        template = 'bootstrap3' if template is None else template.setting_value
        db_theme = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'admin.theme').first()
        theme = 'darkly' if db_theme is None else db_theme.setting_value
        form = forms.theme.Form()
        themes = os.listdir(
            os.path.join(os.path.dirname(flask_admin.__file__), 'static/bootstrap/{}/swatch/'.format(template))
        )
        themes.remove(theme)
        themes.insert(0, theme)
        form.theme.choices = themes
        if form.validate_on_submit():
            to_add = db_theme is None
            db_theme = (
                cms.Settings(setting_value=form.theme.data,
                             setting_name='admin.theme') if db_theme is None else db_theme
            )
            db_theme.setting_value = form.theme.data
            if to_add:
                Database.session.add(db_theme)
            Database.session.commit()
            app: Flask = Process.get()
            app.config['FLASK_ADMIN_SWATCH'] = db_theme.setting_value
            logging.info("{}: {}".format(__name__, request.referrer))
            return redirect(request.referrer)
        return self.render('admin/theme.html', title="Admin theme", selector=form, menu=self.submenu)

    @login_required
    @expose('/site/', methods=['GET', 'POST'])
    def site(self):
        db_theme = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'site.theme').first()
        theme = 'default' if db_theme is None else db_theme.setting_value
        form = forms.theme.Form()
        themes = form.theme.choices = os.listdir(
            os.path.join(Environment.SERVER_DATA['TEMPLATE_PATH'], 'themes')
        )
        themes.remove(theme)
        themes.insert(0, theme)
        form.theme.choices = themes
        if form.validate_on_submit():
            to_add = db_theme is None
            db_theme = (
                cms.Settings(setting_value=form.theme.data, setting_name='site.theme') if db_theme is None else db_theme
            )
            db_theme.setting_value = form.theme.data
            if to_add:
                Database.session.add(db_theme)
            Database.session.commit()
            logging.info("{}: {}".format(__name__, request.referrer))
            return redirect(request.referrer)
        return self.render('admin/site/theme.html', title="Site theme", selector=form, menu=self.submenu)
