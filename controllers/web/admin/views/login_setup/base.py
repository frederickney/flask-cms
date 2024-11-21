# coding: utf-8

import logging
from flask_admin import BaseView, expose
from flask_login import current_user, login_user, logout_user
from flask import url_for, redirect, request, flash, current_app
from Crypto.Hash import SHA512
from models import forms

from flask_framework.Database import Database
from flask_framework.Utils.Auth import admin_login_required as login_required
from models.persistent import cms


class Login(BaseView):

    def __init__(self):
        """

        :param manager:
        :type manager: flask_login.LoginManager
        """
        super(Login, self).__init__(endpoint='admin:login:base', url='/admin/base/')

    @expose('/', methods=['GET'])
    def index(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin'))
        else:
            next = request.args.get('next', None)
            if next:
                return redirect(url_for('admin:login:base.login') + "?next={}".format(next))
            return redirect(url_for('admin:login:base.login'))

    @expose('/login/', methods=['GET'])
    def login(self):
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('admin'))
        else:
            return self.render(
                current_app.config.get(
                    "FLASK_CMS_BASE_ADMIN_LOGIN_TEMPLATE",
                    current_app.config['BASE_LOGIN_TEMPLATE']
                ),
                form=forms.login.Form()
            )

    @expose('/login/', methods=['POST'])
    def send(self):
        form = forms.login.Form()
        if form.validate_on_submit():
            user = Database.session.query(cms.Users).filter(cms.Users.email == form.email.data).first()
            hash = SHA512.new()
            hash.update(bytes(form.password.data, 'utf-8'))
            logging.debug(user)
            if user:
                if user.password == hash.hexdigest():
                    login_user(user)
                    flash('Logged in successfully.')
                    next = request.args.get('next')
                    return redirect(next or request.referrer or url_for('admin'))
                flash('User.Invalid', 'warning')
            else:
                flash('User.Missing.', 'warning')
        return redirect(url_for('admin:login.error'))

    @expose('/fail/', methods=['POST'])
    def error(self):
        return redirect(url_for('admin:login.index'))

    @expose('/logout/', methods=['POST', 'GET'])
    @login_required
    def logout(self):
        logout_user()
        flash('logged out')
        return redirect(url_for('admin:login.index'))

    @staticmethod
    def user(id):
        logging.info("{}: {}".format(__name__, id))
        from models.persistent import cms
        user = Database.session.query(cms.Users).filter(cms.Users.id == id).first()
        return user

    @staticmethod
    def redirect_login():
        if 'admin' in request.url:
            return redirect(url_for('admin:login.index') + "?next={}".format(request.url))
        else:
            return redirect(url_for('login') + "?next={}".format(request.url))