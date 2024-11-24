# coding: utf-8

import logging

from flask import request
from flask_framework.Server import Process


class Controller(object):

    @staticmethod
    def connect():
        """
        from . import ThreadingController
        try:
            ThreadingController.GraphManager.init()
        except Exceptions.RuntimeExceptions.RuntimeException as e:
            logging.debug(e)
        try:
            ThreadingController.GraphManager.start_all()
        except Exceptions.RuntimeExceptions.RuntimeException as e:
            logging.debug(e)
        """
        pass

    @staticmethod
    def test():
        logging.debug('recv event: test')
        Process.get_ws().emit('ack-test', {'ack': 'ok'})

    @staticmethod
    def disconnect():
        pass

    @staticmethod
    def errors(e):
        logging.error(request.event['message'])
        logging.error(request.event['args'])
        logging.error(e)
