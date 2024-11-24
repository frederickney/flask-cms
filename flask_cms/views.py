# coding: utf-8

__author__ = 'Frédérick NEY'

import logging
import os
import flask_admin


class BaseView(flask_admin.BaseView):

    def create_blueprint(self, admin):
        """

        :param admin:
        :type admin: flask_admin.Admin
        :return:
        :rtype: flask.Blueprint
        """
        self.static_folder = os.path.join(os.path.dirname(__file__), 'static')
        self.static_url_path = 'files'
        bp = super(BaseView, self).create_blueprint(admin)
        bp.template_folder = os.path.join(os.path.dirname(__file__), 'template')
        return bp
