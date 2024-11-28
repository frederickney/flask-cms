# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask import redirect, url_for, request, flash
from flask_admin import expose
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models import forms
from flask_cms.models.persistent import cms
from .content import Content


class Pages(Content):

    submenu = [
        {'name': 'List pages', 'endpoint': 'admin:pages.index'},
        {'name': 'Add page', 'endpoint': 'admin:pages.add'},
    ]

    def __init__(self):
        self.type = Pages.__name__.lower()
        super(Pages, self).__init__(endpoint='admin:pages', url='/admin/pages/')
        Process.login_manager().blueprint_login_views.update({'admin:pages': "admin:login.index"})
        Process._csrf.exempt("{}.edit".format(__name__))

    @expose('/')
    @login_required
    def index(self):
        pages = Database.session.query(cms.Contents).filter(
            cms.Contents.type == self.type
        ).order_by(
            cms.Contents.url
        ).all()
        _forms = list()
        for page in pages:
            form = forms.edit.Form()
            form.content.data = page.id
            _forms.append(form)
        return self.render(
            'admin/page/index.html',
            forms=_forms,
            module=self.type,
            menu=self.submenu,
            pages=pages,
        )

    @expose('/add/', methods=['GET'])
    @login_required
    def add(self):
        plugins = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'tinymce.plugins').first()
        toolbar = Database.session.query(cms.Settings).filter(cms.Settings.setting_name == 'tinymce.toolbar').first()
        form = forms.edit.Content()
        form.type.data = self.type
        contents = Database.session.query(cms.Contents).all()
        pages = [(page.id, page.title) for page in contents]
        pages.insert(0, ('', '--- Select ---'))
        form.parent.choices = pages
        return self.render(
            'admin/edit/pages.html',
            form=form,
            module=self.type,
            menu=self.submenu,
            plugins=plugins,
            toolbar=toolbar
        )
