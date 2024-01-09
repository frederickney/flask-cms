# coding : utf-8

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
        del session['oidc_csrf_token']
        del session['oidc_id_token']
        return LDAP.logout()

    @staticmethod
    @login_required
    def test():
        return jsonify({'welcome': 'ok'})