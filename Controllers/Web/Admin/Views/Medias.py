from flask_admin import BaseView, expose
from flask_login import login_required
from .Content import Content
from flask_framework.Database import Database
from flask_framework.Config import Environment
import logging


class Medias(Content):

    submenu = [
        {'name': 'List Medias', 'endpoint': 'admin#medias#index'},
        {'name': 'Add', 'endpoint': 'admin#medias#add'},
    ]

    def __init__(self):
        self.type = Medias.__name__.lower()
        super(Medias, self).__init__(endpoint='admin#medias', url='/admin/medias/')

    @login_required
    @expose('/')
    def index(self):
        from Models.Persistent.cms import Contents
        from Models.Forms.edit import Form
        medias = Database.get_session_by_name('cms').query(Contents)\
            .filter(Contents.type == self.type)\
            .all()
        forms = list()
        for media in medias:
            form = Form()
            form.content.data = media.id
            print(form.content)
            forms.append(form)
        return self.render('admin/medias.html', medias=medias, forms=forms, menu=self.submenu)

    @login_required
    @expose('/add/', methods=['POST'])
    def upload(self):
        import os
        from shutil import copyfile
        from datetime import datetime
        from Models.Forms.upload import Process
        from flask import jsonify, url_for
        from flask import request, flash, redirect, Response
        form = Process()
        form.ext.data = 'medias'
        if form.validate_on_submit():
            from Models.Persistent.cms import Contents
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
                Contents(
                    title=file.filename,
                    type=self.type,
                    activated=False,
                    url='uploads/{}/{}/{}'.format(date.year, date.month, file.filename)
                )
            )
            if url_for('admin#medias#add') not in request.referrer:
                return jsonify(
                    {'file': url_for('static', filename='uploads/{}/{}/{}'.format(date.year, date.month, file.filename))}
                )
            else:
                flash('Upload success')
                return redirect(url_for('admin#medias#add'))
        return Response(status=400)

    @login_required
    @expose('/delete/', methods=['POST'])
    def delete(self):
        import os
        from flask import Response
        from Models.Forms.upload import Delete
        from Models.Persistent.cms import Contents
        form = Delete()
        if form.validate_on_submit():
            content = Database.session.query(Contents).filter(Contents.id == form.content.data).first()
            directory = os.path.join(Environment.SERVER_DATA['STATIC_PATH'])
            try:
                os.remove(os.path.join(directory, content.url))
            except Exception as e:
                logging.warning(e)
            return super(Medias, self).delete()
        return Response(status=400)
