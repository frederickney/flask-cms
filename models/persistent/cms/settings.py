# coding: utf-8


__author__ = 'Frederick NEY'

from flask_framework.Database import Database
from sqlalchemy import Column, Integer, VARCHAR, TEXT, ForeignKey, BIGINT


class Settings(Database.Model):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, nullable=False, default=None, autoincrement=True)
    plugin_id = Column(BIGINT, ForeignKey('plugins.id'), nullable=True)
    setting_name = Column(VARCHAR(256), primary_key=True, nullable=False, default=None)
    setting_value = Column(TEXT(4096))
