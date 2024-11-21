# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import  expose
from flask_login import login_required
import flask
from .Content import Content


class Plugins(Content):


    submenu = [
        {'name': 'List Plugins', 'endpoint': 'admin#plugins#index'},
        {'name': 'Upload', 'endpoint': 'admin#plugins#add'},
    ]

    def __init__(self):
        self.type = Plugins.__name__.lower()
        super(Plugins, self).__init__(endpoint='admin#plugins', url='/admin/plugins/')

    @expose('/', methods=['GET'])
    @login_required
    def index(self):
        from flask_framework import Extensions
        from Models.Forms.plugins import Enable
        from Models.Forms.plugins import Delete
        from Models.Forms.plugins import Disable
        from flask_framework.Extensions.loader import module
        exts = []
        for ext in Extensions.all():
            delete = Delete()
            delete.Extension.data = ext
            enable = Enable()
            enable.Extension.data = ext
            disable = Disable()
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
        from Models.Forms.upload import Plugin
        return self.render('admin/upload/index.html', menu=self.submenu, form=Plugin(), module=self.type)

    @expose('/delete/', methods=['POST'])
    @login_required
    def delete(self):
        pass

    @expose('/enable/', methods=['POST'])
    @login_required
    def enable(self):
        from flask import request
        from Models.Forms.plugins import Enable
        from flask_framework.Extensions.loader import installer
        from flask_framework.Extensions.loader import module as retriever
        form = Enable()
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
        from Models.Forms.plugins import Disable
        from flask_framework.Extensions.loader import module as retriever
        form = Disable()
        if form.validate_on_submit():
            module = form.Extension.data
            mod = retriever(module)
            mod.Loader.disable()
            return flask.redirect(request.referrer)
        else:
            module = form.Extension.data
            flask.flash('Could not load module %s' % module)
        return flask.redirect(request.referrer)
