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
from flask_cms.views import BaseView


class Content(BaseView):
    type = 'page'

    def __init__(self, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)

    @login_required
    @expose('/add/', methods=['GET'])
    def add(self):
        form = forms.upload.Process()
        form.ext.data = self.type
        return self.render('admin/upload/index.html', form=form, menu=self.submenu, module=self.type)

    @login_required
    @expose('/edit/', methods=['GET'])
    def edit(self):
        from flask import redirect, request
        content = forms.edit.Form(request.args, meta={'csrf': False})
        if content.validate():
            from flask_framework.Database import Database
            content = Database.session.query(cms.Contents).filter(cms.Contents.id == content.content.data).first()
            form = forms.edit.Content()
            form.content.data = content.content
            form.title.data = content.title
            form.url.data = content.url
            form.publish.data = content.activated
            form.type.data = self.type
            form.id.data = content.id
            contents = Database.session.query(cms.Contents).order_by(
                cms.Contents.url
            ).order_by(
                cms.Contents.type
            ).all()
            pages = [(page.id, page.title) for page in contents]
            pages.insert(0, ('', '--- Select ---'))
            if content.parent_id:
                pages.remove((content.parent_id, content.parent.title))
                pages.insert(0, (content.parent_id, content.parent.title))
            form.parent.choices = pages
            return self.render('admin/edit/{}.html'.format(self.type), form=form, content=content)
        return redirect(request.referrer)

    @login_required
    @expose('/delete/', methods=['POST'])
    def delete(self):
        from flask import redirect, url_for
        form = forms.upload.Delete()
        if form.validate_on_submit():
            from flask_framework.Database import Database
            content = Database.session.query(cms.Contents).filter(cms.Contents.id == form.content.data).first()
            for meta in content.metas:
                Database.session.delete(meta)
            for child in content.childs:
                child.parent_id = None
            Database.session.commit()
            Database.session.delete(content)
            Database.session.commit()
        return redirect(url_for(self.endpoint + '.index'))

    @expose('/save/', methods=['POST'])
    @login_required
    def save(self):
        update = forms.edit.Content()
        new = forms.edit.NewContent()
        contents = Database.session.query(cms.Contents).all()
        pages = [(page.id, page.title) for page in contents]
        update.parent.choices = pages
        new.parent.choices = pages
        if update.validate_on_submit():
            if update.type.data == self.type:
                content = Database.session.query(cms.Contents).filter(cms.Contents.id == update.id.data).first()
                logging.info("{}: {}".format(__name__, type(update.parent.data)))
                logging.info("{}: {}".format(__name__, update.parent.data))
                if content:
                    content.parent_id = (
                        None if len(update.parent.data) == 0 else
                        None if not update.parent.data.isnumeric() else
                        int(update.parent.data)
                    )
                    content.url = update.url.data
                    content.title = update.title.data
                    content.content = update.content.data
                    content.activated = update.publish.data
        elif new.validate_on_submit():
            if new.type.data == self.type:
                logging.info("{}: {}".format(__name__, request.data))
                logging.info("{}: {}".format(__name__, request.form))
                Database.session.add(
                    cms.Contents(
                        title=new.title.data,
                        url=new.url.data,
                        content=new.content.data,
                        activated=new.publish.data,
                        type=self.type,
                        parent_id=(
                            None if len(update.parent.data) == 0 else
                            None if not update.parent.data.isnumeric() else
                            int(update.parent.data)
                        )
                    )
                )
                Database.session.commit()
        else:
            flash(new.errors)
            redirect(url_for('admin:pages.add'))
        return redirect(url_for('admin:pages.index'))