# coding: utf-8


__author__ = 'Frederick NEY'

from flask import render_template as template


def handle(error):
    return template('40x.html', title=error)
