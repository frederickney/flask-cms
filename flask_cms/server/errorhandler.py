# coding: utf-8

__author__ = 'Frederick NEY'


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
        from flask_cms import controllers
        server.register_error_handler(401, controllers.web.errors.unauthorized.handle)
        server.register_error_handler(404, controllers.web.render.render_or_not_found)
