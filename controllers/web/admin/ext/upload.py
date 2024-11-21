# coding: utf-8


__author__ = 'Frederick NEY'


from apscheduler.jobstores.base import ConflictingIdError
from flask import render_template as template
from flask import redirect, url_for
from flask_login import login_required
from Models import Forms
import logging
from flask import request
import os
from flask_framework.Config import Environment


class UploadController(object):

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
        form = Forms.upload.Form()
        return template('admin/upload/index.html', form=form)

    @staticmethod
    @login_required
    def upload():
        form = Forms.upload.Form()
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(Environment.SERVER_DATA['UPLOAD_FILE_DIR'], file.filename))
            return redirect(url_for('admin#upload#process', type='ext'), code=307)
        return template('admin/upload/success.jinja2')

    @staticmethod
    @login_required
    def process():
        form = Forms.upload.Form()
        if form.validate_on_submit():
            if 'type' in request.args:
                if request.args['type'] in UploadController.types:
                    if request.args['type'] == UploadController.ext:
                        UploadController.install_ext(form.file.data.filename)
                    if request.args['type'] == UploadController.theme:
                        UploadController.install_theme(form.file.data.filename)
                    if request.args['type'] == UploadController.file:
                        UploadController.store_file(form.file.data.filename)
                    if request.args['type'] == UploadController.doc:
                        UploadController.store_doc(form.file.data.filename)
                    if request.args['type'] == UploadController.image:
                        UploadController.store_image(form.file.data.filename)
                    if request.args['type'] == UploadController.video:
                        UploadController.store_video(form.file.data.filename)
                    return redirect(url_for('admin#upload#success'))
        return redirect('admin#upload')

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
