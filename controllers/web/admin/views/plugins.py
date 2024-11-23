# coding: utf-8


__author__ = 'Frederick NEY'

import flask
from flask_admin import expose
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from models import forms
from .content import Content


class Plugins(Content):
    submenu = [
        {'name': 'List Plugins', 'endpoint': 'admin:plugins.index'},
        {'name': 'Upload', 'endpoint': 'admin:plugins.add'},
    ]

    def __init__(self):
        self.type = Plugins.__name__.lower()
        super(Plugins, self).__init__(endpoint='admin:plugins', url='/admin/plugins/')
        Process.login_manager().blueprint_login_views.update({'admin:plugins': "admin:login.index"})

    @expose('/', methods=['GET'])
    @login_required
    def index(self):
        from flask_framework import Extensions
        from flask_framework.Extensions.loader import module
        exts = []
        for ext in Extensions.all():
            delete = forms.plugins.Delete()
            delete.Extension.data = ext
            enable = forms.plugins.Enable()
            enable.Extension.data = ext
            disable = forms.plugins.Disable()
            disable.Extension.data = ext
            exts.append({
                'name': ext,
                'delete_form': delete,
                'disable_form': disable,
                'enable_form': enable,
                'enabled': module(ext).Loader.enabled()
            })
        return self.render('admin/plugins/list.html', menu=self.submenu, exts=exts)

    @expose('/add/', methods=['GET'])
    @login_required
    def add(self):
        return self.render(
            'admin/upload/index.html',
            menu=self.submenu,
            form=forms.upload.Plugin(),
            module=self.type
        )

    @expose('/delete/', methods=['POST'])
    @login_required
    def delete(self):
        pass

    @expose('/enable/', methods=['POST'])
    @login_required
    def enable(self):
        from flask import request
        from flask_framework.Extensions.loader import installer
        from flask_framework.Extensions.loader import module as retriever
        form = forms.plugins.Enable()
        if form.validate_on_submit():
            module = form.Extension.data
            installer(module)
            mod = retriever(module)
            mod.Loader.enable()
            return flask.redirect(request.referrer)
        else:
            module = form.Extension.data
            flask.flash('Could not load module %s' % module)
        return flask.redirect(request.referrer)

    @expose('/disable/', methods=['POST'])
    @login_required
    def disable(self):
        from flask import request
        from flask_framework.Extensions.loader import module as retriever
        form = forms.plugins.Disable()
        if form.validate_on_submit():
            module = form.Extension.data
            mod = retriever(module)
            mod.Loader.disable()
            return flask.redirect(request.referrer)
        else:
            module = form.Extension.data
            flask.flash('Could not load module %s' % module)
        return flask.redirect(request.referrer)
