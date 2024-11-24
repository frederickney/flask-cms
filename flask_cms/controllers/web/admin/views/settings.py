# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask import request, redirect, url_for
from flask_admin import BaseView, expose
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models import forms
from flask_cms.models.persistent import cms


class Settings(BaseView):
    submenu = [
        {'name': 'General', 'endpoint': 'admin:settings.setting'},
        {'name': 'Users', 'endpoint': 'admin:settings:users.all'},
    ]

    def __init__(self):
        super(Settings, self).__init__(endpoint='admin:settings', url='/admin/settings/')
        Process.login_manager().blueprint_login_views.update({'admin:settings': "admin:login.index"})

    @expose('/', methods=['GET', 'POST'])
    @login_required
    def index(self):
        form = forms.settings.CmsSettings()
        if form.validate_on_submit():
            setting = cms.Settings(
                setting_name=form.Name.data,
                setting_value=form.Value.data,
            )
            Database.session.add(setting)
            Database.session.commit()
        return self.render(
            'admin/setup.html',
            menu=self.submenu,
            form=forms.settings.CmsSettings(),
            settings=Database.session.query(cms.Settings).all()
        )

    @expose('/general/', methods=['GET', 'POST'])
    @login_required
    def setting(self):
        form = forms.settings.CmsSettings()
        if form.validate_on_submit():
            setting = cms.Settings(
                setting_name=form.Name.data,
                setting_value=form.Value.data,
            )
            Database.session.add(setting)
            Database.session.commit()
            return redirect(request.referrer)
        settings = []
        for setting in Database.session.query(cms.Settings).filter(cms.Settings.plugin_id == None).all():
            update = forms.settings.CmsSettingsUpdate()
            update.ID.data = setting.id
            update.Value.label = setting.setting_name
            update.Value.data = setting.setting_value
            delete = forms.settings.Delete()
            delete.ID.data = setting.id
            settings.append({
                'delete': delete,
                'update': update,
            })
        return self.render(
            'admin/settings/general.html',
            menu=self.submenu,
            form=forms.settings.CmsSettings(),
            settings=settings,
        )

    @expose('/general/delete/', methods=['POST'])
    @login_required
    def delete(self):
        form = forms.settings.Delete()
        if form.validate_on_submit():
            logging.info("{}: deleting {}".format(__name__, form.ID.data))
            Database.session.query(cms.Settings).filter(cms.Settings.id == form.ID.data).delete()
            Database.session.commit()
        return redirect(request.referrer or url_for('admin:settings.setting'))

    @expose('/general/update/', methods=['POST'])
    @login_required
    def update(self):
        form = forms.settings.CmsSettingsUpdate()
        if form.validate_on_submit():
            logging.info("{}: deleting {}".format(__name__, form.ID.data))
            setting = Database.session.query(cms.Settings).filter(cms.Settings.id == form.ID.data).first()
            setting.setting_value = form.Value.data
            Database.session.commit()
        return redirect(request.referrer or url_for('admin:settings.setting'))
