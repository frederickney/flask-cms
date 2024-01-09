# coding : utf-8

__author__ = 'Frederick NEY'


from flask import g, session, jsonify, request
import flask
import logging
from flask import redirect, url_for
from flask_framework.Server import Process


class Controller(object):

    @staticmethod
    def index():
        session.set()
        logging.debug(session.get('oidc_id_token'))
        next = request.args.get('next')
        return flask.redirect(next or request.referrer or flask.url_for('home'))

    @staticmethod
    def logout():
        Process.openid.logout()
        return redirect(url_for('home'))
