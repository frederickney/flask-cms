# coding: utf-8


__author__ = 'Frederick NEY'


from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN

from flask_framework.Database import Database
from flask_framework.Database.decorators import secured


class Users(Database.Model):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, default=None)
    email = Column(VARCHAR(256))
    firstname = Column(VARCHAR(256))
    lastname = Column(VARCHAR(256))
    password = Column(VARCHAR(512))
    is_active = Column(BOOLEAN())
    is_admin = Column(BOOLEAN())
    is_authenticated = False
    is_anonymous = False

    @secured("id")
    def __init__(self):
        self.id = property(self.get_id, self.set_id)

    def get_id(self, value):
        return self._id

    def set_id(self, value):
        from flask_framework.Exceptions.QueryExceptions import PrimaryKeyChangeException
        raise PrimaryKeyChangeException("Trying to change read only primary key id of {}[{}] by {}".format(Users.__name__, self._id, value))