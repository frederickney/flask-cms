# coding: utf-8


__author__ = 'Frederick NEY'

from flask_admin import BaseView, expose
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.models import forms
from flask_cms.models.persistent import cms


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
        content = forms.edit.Form()
        print(request.args)
        if content.validate_on_submit():
            from flask_framework.Database import Database
            content = Database.session.query(cms.Contents).filter(cms.Contents.id == content.content.data).first()
            return self.render('admin/edit/{}.html'.format(self.type), form=forms.edit.Content(), content=content)
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
            Database.session.delete(content)
            Database.session.commit()
        return redirect(url_for(self.endpoint + '.index'))

    @expose('/save/', methods=['POST'])
    @login_required
    def save(self):
        pass
