# coding: utf-8


__author__ = 'Frederick NEY'


from flask import render_template as template
from flask import redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
import flask_framework.Server as Server
from Models import Forms, Persistent
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
        import Controllers
        Server.Process._manager = LoginManager()
        Server.Process._manager.init_app(app=Server.Process.get())
        Server.Process._manager.user_loader(cls.user)
        Server.Process._manager.unauthorized_handler(cls.index)
        Server.Process.get().add_url_rule('/login/', 'login', Controllers.Web.Login.LocalLoginController.index, methods=['GET'])
        Server.Process.get().add_url_rule('/login/', 'login.send', Controllers.Web.Login.LocalLoginController.login, methods=['POST'])
        Server.Process.get().add_url_rule('/login/failed/', 'login.fails', Controllers.Web.Login.LocalLoginController.error, methods=['GET'])
        Server.Process.get().add_url_rule('/logout/', 'logout', Controllers.Web.Login.LocalLoginController.logout, methods=['POST'])
        Controllers.Web.Admin.setup()

    @classmethod
    def user(cls, id):
        user = Database. session.query(Persistent.cms.Users).filter(Persistent.cms.Users.id == id).first()
        user.is_authenticated = True
        return user

    @classmethod
    def index(cls):
        form = Forms.login.Form()
        return template('login/index.html', form=form, theme='default')

    @classmethod
    def login(cls):
        form = Forms.login.Form()
        logging.debug('form token %s' % form.csrf_token)
        logging.debug('recv token %s' % form.csrf_token.data)
        if form.validate_on_submit():
            user = Database.session.query(Persistent.cms.Users).filter(Persistent.cms.Users.email == form.email.data).first()
            hash = SHA512.new()
            hash.update(bytes(form.password.data, 'utf-8'))
            logging.debug(user)
            if user:
                if user.password == hash.hexdigest():
                    user.is_authenticated = True
                    login_user(user)
                    flask.flash('Logged in successfully.')
                    next = request.args.get('next')
                    return flask.redirect(next or request.referrer or flask.url_for('home'))
                flash('User.Invalid', 'warning')
            else:
                flash('User.Missing.', 'warning')
        return redirect(url_for('login.fails'))

    @classmethod
    def error(cls):
        return redirect(url_for('login'))

    @classmethod
    @login_required
    def logout(cls):
        logout_user()
        flask.flash('Invalid username / password ')
        return redirect(url_for('home'))
