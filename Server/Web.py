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
        import Controllers
        server.add_url_rule('/', "home", Controllers.Web.HomeController.default, methods=["GET"])
        Controllers.Web.Login.LocalLoginController.setup()
        server.add_url_rule('/openid/', 'openid', Controllers.Web.Login.OpenIdLoginController.index, methods=['GET', 'POST'])
        server.add_url_rule('/openid/logout/', 'openidlogout', Controllers.Web.Login.OpenIdLoginController.logout, methods=['GET', 'POST'])
        server.add_url_rule('/access/ad', 'ad-login', Controllers.Web.Login.ADLoginController.login, methods=['GET', 'POST'])
        server.add_url_rule('/access/ad/logout', 'ad-logout', Controllers.Web.Login.ADLoginController.logout, methods=['GET', 'POST'])
        server.add_url_rule('/test', 'test', Controllers.Web.Login.ADLoginController.test, ['GET'])
        return

