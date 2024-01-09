# coding: utf-8


__author__ = 'Frederick NEY'


from flask_admin import BaseView, expose
from flask_login import login_required


class Content(BaseView):

    type = 'page'

    def __init__(self, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)

    @login_required
    @expose('/add/', methods=['GET'])
    def add(self):
        from Models.Forms.upload import Process
        form = Process()
        form.ext.data = self.type
        return self.render('admin/upload/index.html', form=form, menu=self.submenu, module=self.type)

    @login_required
    @expose('/edit/', methods=['GET'])
    def edit(self):
        from flask import redirect, request, flash
        from Models.Forms.edit import Content
        from Models.Forms.edit import Form
        content = Form()
        print(request.data)
        print(request.form)
        print(request.json)
        print(content.content)
        if content.validate_on_submit():
            from flask_framework.Database import Database
            from Models.Persistent.cms import Contents
            content = Database.session.query(Contents).filter(Contents.id == content.content.data).first()
            return self.render('admin/edit/{}.html'.format(self.type), form=Content(), content=content)
        return redirect(request.referrer)

    @login_required
    @expose('/delete/', methods=['POST'])
    def delete(self):
        from flask import redirect, url_for, request
        from Models.Forms.upload import Delete
        form = Delete()
        print(request.data)
        print(request.form)
        print(request.json)
        if form.validate_on_submit():
            from flask_framework.Database import Database
            from Models.Persistent.cms import Contents
            content = Database.session.query(Contents).filter(Contents.id == form.content.data).first()
            for meta in content.metas:
                Database.session.delete(meta)
            Database.session.delete(content)
        return redirect(url_for(self.endpoint + '.index'))

    @expose('/save/', methods=['POST'])
    @login_required
    def save(self):
        pass