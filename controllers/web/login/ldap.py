# coding: utf-8


__author__ = 'Frederick NEY'


from flask import jsonify, render_template, request, redirect, url_for, session, flash, current_app
from flask_framework.Utils.Auth.ldap import login_required, LDAP


class Controller(object):

    @staticmethod
    def index():
        return render_template('welcome.html')

    @staticmethod
    def login():
        return LDAP.login()

    @staticmethod
    def logout():
        return LDAP.logout()

    @staticmethod
    @login_required
    def test():
        from flask import session
        return jsonify({'welcome': 'ok', 'username' : session.get('username')})