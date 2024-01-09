# coding: utf-8

__author__ = 'Frederick NEY'

from flask import render_template as template, jsonify
from flask import redirect, url_for
from flask import session
from flask_login import login_required, current_user
from Models import Forms


class Controller(object):

    @staticmethod
    def default():
        import logging
        from flask_framework.Server import Process
        links = []
        for rule in Process.get().url_map.iter_rules():
            logging.info((rule.rule, rule.endpoint))
        return template("themes/%s/welcome.html" % 'default', logout=Forms.login.Form())




