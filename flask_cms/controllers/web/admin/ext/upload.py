# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import os

from apscheduler.jobstores.base import ConflictingIdError
from flask import redirect, url_for
from flask import render_template as template
from flask import request
from flask_framework.Config import Environment
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models import forms


class Upload(object):
    ext = 'ext'
    file = 'file'
    video = 'video'
    doc = 'document'
    theme = 'theme'
    image = 'image'
    types = {file, ext, video, image, doc, theme}

    @staticmethod
    @login_required
    def index():
        form = forms.upload.Form()
        return template('admin/upload/index.html', form=form)

    @staticmethod
    @login_required
    def upload():
        form = forms.upload.Form()
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(Environment.SERVER_DATA['UPLOAD_FILE_DIR'], file.filename))
            return redirect(url_for('admin:upload.process', type='ext'), code=307)
        return template('admin/upload/success.jinja2')

    @staticmethod
    @login_required
    def process():
        form = forms.upload.Form()
        if form.validate_on_submit():
            if 'type' in request.args:
                if request.args['type'] in Upload.types:
                    if request.args['type'] == Upload.ext:
                        Upload.install_ext(form.file.data.filename)
                    if request.args['type'] == Upload.theme:
                        Upload.install_theme(form.file.data.filename)
                    if request.args['type'] == Upload.file:
                        Upload.store_file(form.file.data.filename)
                    if request.args['type'] == Upload.doc:
                        Upload.store_doc(form.file.data.filename)
                    if request.args['type'] == Upload.image:
                        Upload.store_image(form.file.data.filename)
                    if request.args['type'] == Upload.video:
                        Upload.store_video(form.file.data.filename)
                    return redirect(url_for('admin:upload.success'))
        return redirect('admin:upload')

    @staticmethod
    @login_required
    def success():
        return template('admin/upload/success.jinja2')

    @staticmethod
    def install_theme(ext):
        pass

    @staticmethod
    def install_ext(ext):
        import zipfile
        from flask_framework.Server import Process
        archive = zipfile.ZipFile(os.path.join(Environment.SERVER_DATA['UPLOAD_FILE_DIR'], ext), 'r')
        archive.extractall(os.path.join(os.curdir, os.path.join('src/Extensions', ext.split('.')[0])))
        try:
            import uuid
            Process.add_parallel_task('Task.Plugins.load')
        except ConflictingIdError as e:
            logging.info('task: "Task.Plugins.load" skipped')
            logging.info(e)
        pass

    @staticmethod
    def store_file(ext):
        pass

    @staticmethod
    def store_doc(ext):
        pass

    @staticmethod
    def store_video(ext):
        pass

    @staticmethod
    def store_image(ext):
        pass
