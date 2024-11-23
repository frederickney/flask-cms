# coding: utf-8


__author__ = 'Frederick NEY'

from datetime import datetime

from flask_framework.Database import Database
from sqlalchemy import Column, VARCHAR, ForeignKey, BOOLEAN, BIGINT, TEXT, DateTime
from sqlalchemy.orm import relationship


class Contents(Database.Model):
    __tablename__ = 'content'

    id = Column(BIGINT, primary_key=True, nullable=False, default=None, autoincrement=True)
    url = Column(VARCHAR(256), primary_key=True, nullable=True, default=None)
    title = Column(VARCHAR(256), primary_key=True, nullable=False, default=None)
    content = Column(TEXT)
    activated = Column(BOOLEAN, nullable=False, default=False)
    type = Column(VARCHAR(32), nullable=False)
    parent_id = Column(BIGINT, ForeignKey('content.id'), nullable=True)
    parent = relationship('Contents')
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now)
    metas = relationship("Metadata", uselist=True)

    def __repr__(self):
        return self.title
