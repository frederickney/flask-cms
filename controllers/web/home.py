# coding: utf-8


__author__ = 'Frederick NEY'


from flask import render_template as template
from flask_login import login_required, current_user
from models import forms


class Controller(object):

    @staticmethod
    @login_required
    def test():
        return template("themes/%s/welcome.html" % 'default', logout=forms.login.Form())

    @staticmethod
    def default():
        import logging
        from flask_framework.Server import Process
        links = []
        logging.info(current_user)
        for rule in Process.get().url_map.iter_rules():
            logging.info((rule.rule, rule.endpoint))
        return template("themes/%s/welcome.html" % 'default', logout=forms.login.Form())




