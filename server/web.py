# coding: utf-8

__author__ = 'Frederick NEY'

import flask_cms


class Route(object):
    """
    Class that will configure all web based routes for the server
    """

    def __init__(self, server):
        """
        Constructor
        :param server: Flask server
        :type server: flask.Flask
        :return: Route object
        """
        flask_cms.server.web.Route(server)
        import controllers
        server.add_url_rule('/test', "test", controllers.web.home.test, methods=["GET"])
        return
