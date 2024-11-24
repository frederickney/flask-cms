# coding: utf-8


__author__ = 'Frederick NEY'

import flask_cms


class Handler(object):

    def __init__(self, socketio):
        """

        :param socketio:
        :type socketio: flask_socketio.SocketIO
        """
        flask_cms.server.socket.Handler(socketio)
