# coding: utf-8


__author__ = 'Frederick NEY'

from flask_framework.Database import Database
from sqlalchemy import Column, VARCHAR, ForeignKey, BIGINT, TEXT


class Metadata(Database.Model):
    __tablename__ = 'metadata'

    id = Column(BIGINT, primary_key=True, nullable=False, default=None, autoincrement=True)
    content_id = Column(BIGINT, ForeignKey('content.id'), nullable=False)
    key = Column(VARCHAR(256), primary_key=True, nullable=False)
    value = Column(TEXT, nullable=False)
