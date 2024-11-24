# coding: utf-8


__author__ = 'Frederick NEY'

from flask_framework.Database import Database
from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.orm import relationship


class Plugins(Database.Model):
    __tablename__ = 'plugins'

    id = Column(BIGINT, nullable=False, default=None, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(250), nullable=False)
    settings = relationship('Settings', uselist=True)
