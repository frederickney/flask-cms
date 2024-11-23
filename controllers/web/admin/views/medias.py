# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from flask_admin import expose
from flask_framework.Config import Environment
from flask_framework.Database import Database
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from models import forms
from models.persistent import cms
from .content import Content


class Medias(Content):
    submenu = [
        {'name': 'List Medias', 'endpoint': 'admin:medias.index'},
        {'name': 'Add', 'endpoint': 'admin:medias.add'},
    ]

    def __init__(self):
        self.type = Medias.__name__.lower()
        super(Medias, self).__init__(endpoint='admin:medias', url='/admin/medias/')
        Process.login_manager().blueprint_login_views.update({'admin:medias': "admin:login.index"})

    @login_required
    @expose('/')
    def index(self):
        medias = Database.get_session_by_name('cms').query(cms.Contents) \
            .filter(cms.Contents.type == self.type) \
            .all()
        _forms = list()
        for media in medias:
            form = forms.edit.Form()
            form.content.data = media.id
            _forms.append(form)
        return self.render('admin/medias.html', medias=medias, forms=_forms, menu=self.submenu)

    @login_required
    @expose('/add/', methods=['POST'])
    def upload(self):
        import os
        from shutil import copyfile
        from datetime import datetime
        from flask import jsonify, url_for
        from flask import request, flash, redirect, Response
        form = forms.upload.Process()
        form.ext.data = 'medias'
        if form.validate_on_submit():
            file = form.file.data
            date = datetime.now().date()
            directory = os.path.join(Environment.SERVER_DATA['STATIC_PATH'], 'uploads', str(date.year), str(date.month))
            if not os.path.isdir(directory):
                os.makedirs(directory, mode=755)
            file.save(os.path.join(Environment.SERVER_DATA['UPLOAD_FILE_DIR'], file.filename))
            copyfile(
                os.path.join(Environment.SERVER_DATA['UPLOAD_FILE_DIR'], file.filename),
                os.path.join(directory, file.filename)
            )
            Database.session.add(
                cms.Contents(
                    title=file.filename,
                    type=self.type,
                    activated=False,
                    url='uploads/{}/{}/{}'.format(date.year, date.month, file.filename)
                )
            )
            Database.session.commit()
            if url_for('admin:medias.add') not in request.referrer:
                return jsonify(
                    {'file': url_for('static',
                                     filename='uploads/{}/{}/{}'.format(date.year, date.month, file.filename))}
                )
            else:
                flash('Upload success')
                return redirect(url_for('admin:medias.add'))
        return Response(status=400)

    @login_required
    @expose('/delete/', methods=['POST'])
    def delete(self):
        import os
        from flask import Response
        form = forms.upload.Delete()
        if form.validate_on_submit():
            content = Database.session.query(cms.Contents).filter(cms.Contents.id == form.content.data).first()
            directory = os.path.join(Environment.SERVER_DATA['STATIC_PATH'])
            try:
                os.remove(os.path.join(directory, content.url))
            except Exception as e:
                logging.warning(e)
            return super(Medias, self).delete()
        return Response(status=400)
