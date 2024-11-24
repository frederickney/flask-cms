# coding: utf-8

__author__ = 'Frederick NEY'

from flask import render_template as template
from flask_login import login_required

from flask_cms.models import forms


class Controller(object):

    @staticmethod
    def index():
        return

    @staticmethod
    @login_required
    def test():
        import logging
        from flask_framework.Server import Process
        links = []
        for rule in Process.get().url_map.iter_rules():
            logging.info((rule.rule, rule.endpoint))
        return template("themes/%s/welcome.html" % 'default', logout=forms.login.Form())
