# coding: utf-8


__author__ = 'Frederick NEY'


from flask import render_template as template
from flask import redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import flask_framework.Server as Server
from models import forms
from models.persistent import cms
import flask
from flask_framework.Database import Database
from Crypto.Hash import SHA512
import logging
from flask import request, flash


class Controller(object):

    @classmethod
    @Server.deniedwebcall
    def setup(cls):
        """

        :return:
        """
        from flask_framework import Server
        import controllers
        Server.Process._manager = LoginManager()
        Server.Process._manager.init_app(app=Server.Process.get())
        Server.Process._manager.unauthorized_handler(cls.redirect_login)
        Server.Process._manager.user_loader(cls.user)
        Server.Process.get().add_url_rule('/base/login/', 'base.login', controllers.web.login.local.index, methods=['GET'])
        Server.Process.get().add_url_rule('/base/login/', 'base.login.send', controllers.web.login.local.login, methods=['POST'])
        Server.Process.get().add_url_rule('/base/logout/', 'base.logout', controllers.web.login.local.logout, methods=['POST'])
        try:
            Server.Process.get().add_url_rule('/logout/', 'logout', controllers.web.login.local.logout, methods=['POST'])
            Server.Process.get().add_url_rule('/login/', 'login', controllers.web.login.local.index, methods=['GET'])
            Server.Process.get().add_url_rule('/login/', 'base.login.send', controllers.web.login.local.login, methods=['POST'])
        except Exception as e:
            pass

    @classmethod
    def user(cls, id):
        logging.info("{}: {}".format(__class__, id))
        user = Database. session.query(cms.Users).filter(cms.Users.id == id).first()
        user.is_authenticated = True
        return user

    @classmethod
    def index(cls):
        if current_user.is_authenticated:
            flash(u"You are already login in {0}".format(current_user.email))
            return redirect(url_for(current_app.config['BASE_SUCCESS_REDIRECT']))
        form = forms.login.Form()
        return template(current_app.config['BASE_LOGIN_TEMPLATE'], form=form, theme='default')

    @classmethod
    def redirect_login(cls):
        return redirect(url_for('base.login') + "?next={}".format(request.url))

    @classmethod
    def login(cls):
        form = forms.login.Form()
        logging.debug('form token %s' % form.csrf_token)
        logging.debug('recv token %s' % form.csrf_token.data)
        if form.validate_on_submit():
            user = Database.session.query(cms.Users).filter(cms.Users.email == form.email.data).first()
            hash = SHA512.new()
            hash.update(bytes(form.password.data, 'utf-8'))
            logging.debug(user)
            if user:
                if user.password == hash.hexdigest():
                    user.is_authenticated = True
                    login_user(user)
                    flask.flash('Logged in successfully.')
                    next = request.args.get('next')
                    logging.info(next or request.referrer or flask.url_for('home'))
                    return flask.redirect(next or request.referrer or flask.url_for('home'))
                flash('User.Invalid', 'warning')
            else:
                flash('User.Missing.', 'warning')
        return redirect(url_for('local.login'))


    @classmethod
    @login_required
    def logout(cls):
        logout_user()
        flask.flash('logged out')
        return redirect(url_for('home'))
