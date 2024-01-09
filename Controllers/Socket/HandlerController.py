

from flask_socketio import send, emit
from flask import jsonify
import flask_socketio
import json
import Server
import logging


class Controller(object):

    wss: flask_socketio.SocketIO = None

    def __init__(self, wss):
        """

        :param wss:
        :type wss: flask_socketio.SocketIO
        """
        self.wss = wss

    @staticmethod
    def connect():
        """
        try:
            import Task
            Task.WSS.setup(Server.Process.get_ws())
        except Exception as e:
            logging.info('WebSocket already setup')
        try:
            Server.Process.add_cron('Task.WSS.health_check', seconds=30)
        except Exception as e:
            logging.info(e)
        try:
            Server.Process.add_cron('Task.WSS.health_check', id='2', seconds=30)
        except Exception as e:
            logging.info(e)
        try:
            Server.Process.add_cron('Task.WSS.json', id='1', seconds=30)
        except Exception as e:
            logging.info(e)
        """
        pass