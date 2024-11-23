# coding: utf-8


__author__ = 'Frederick NEY'

import json
import logging
from base64 import b64encode
from datetime import datetime

import authlib.jose
import requests
import saml2.saml
from flask import current_app, session
from flask_framework.Database import Database
from flask_login import login_user
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN

import utils.mapper.openid
import utils.mapper.saml


class Users(Database.Model):
    __tablename__ = 'users'
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, default=None)
    email = Column(VARCHAR(256))
    firstname = Column(VARCHAR(256))
    lastname = Column(VARCHAR(256))
    password = Column(VARCHAR(512))
    is_active = Column(BOOLEAN())
    is_admin = Column(BOOLEAN())
    is_anonymous = False
    token: dict = None
    assertion = None
    exp = None

    def __init__(self, **kwargs):
        first = None
        second = None
        last = None
        try:
            super(Users, self).__init__(**kwargs)
            return
        except TypeError as e:
            first = e
            pass
        try:
            logging.info("{}: openid user loading".format(__name__))
            super(Users, self).__init__(**self._load_from_token(**kwargs))
            _user = Database.session.query(Users).filter(Users.email == self.email).first()
            if _user:
                _user = Database.session.query(Users).filter(Users.email == self.email).first()
                self.is_active = _user.is_active
                if self.is_active:

                    _user.is_admin = self.is_admin
                    Database.session.commit()
                else:
                    self.is_admin = _user.is_admin
            else:
                self.is_active = True
                Database.session.add(self)
                Database.session.commit()
            logging.info("{}: openid user loaded".format(__name__))
            return
        except Exception as e:
            second = e
            pass
        try:
            logging.info("{}: saml user loading".format(__name__))
            super(Users, self).__init__(**self._load_from_assertion(**kwargs))
            if Database.session.query(Users).filter(Users.email == self.email).first():
                _user = Database.session.query(Users).filter(Users.email == self.email).first()
                self.is_active = _user.is_active
                if self.is_active:
                    _user.is_admin = self.is_admin
                    Database.session.commit()
                else:
                    self.is_admin = _user.is_admin
            else:
                self.is_active = True
                Database.session.add(self)
                Database.session.commit()
            logging.info("{}: saml user loaded".format(__name__))
            return
        except Exception as e:
            last = e
            pass
        raise Exception(first, second, last)

    def get_id(self):
        return self.token or self.assertion or self.id

    @staticmethod
    @utils.mapper.openid
    def _load_from_token(**kwargs):
        return kwargs

    @staticmethod
    @utils.mapper.saml
    def _load_from_assertion(**kwargs):
        return kwargs

    @staticmethod
    @utils.mapper.openid
    def map_openid(**kwargs):
        return Users(**kwargs)

    @staticmethod
    @utils.mapper.saml
    def map_saml(**kwargs):
        return Users(**kwargs)

    @staticmethod
    def load_from_token(oidc_client, token):
        """

        :param oidc_auth:
        :type oidc_auth: FlaskOAuth2App
        :param token:
        :return:
        """
        if type(token) is str:
            token = token.replace("'", '"')
            token = json.loads(token)
        try:
            if 'id_token' in token:
                userinfo = oidc_client.parse_id_token(token, nonce="")
                userinfo["token"] = token
                user = Users.map_openid(**userinfo)
                if not user.is_authenticated:
                    session.pop("_user_id")
                    refresh = requests.post(oidc_client.load_server_metadata()['token_endpoint'], data={
                        'grant_type': "refresh_token",
                        'refresh_token': token['refresh_token']
                    }, headers={
                        'Authorization': "Basic {}".format(b64encode("{}:{}".format(
                            oidc_client.client_id, oidc_client.client_secret
                        ).encode()).decode('utf-8'))
                    })
                    token = refresh.json()
                    userinfo = oidc_client.parse_id_token(token, nonce="")
                    userinfo["token"] = token
                    user = Users.map_openid(**userinfo)
                    login_user(user, force=True)
                registered_user = Database.session.query(Users).filter(Users.email == user.email).first()
                if registered_user:
                    registered_user.exp = user.exp
                    registered_user.token = user.token
                return registered_user
        except authlib.jose.errors.ExpiredTokenError as e:
            # next ?
            pass
        return None

    @staticmethod
    def load_from_assertion(xml):
        """
        :param xml:
        :return:
        :rtype: SAMLUser
        """
        assertion = saml2.saml.assertion_from_string(xml)
        attributes = {'Role': []}
        for attribute_statement in assertion.attribute_statement:
            for attribute in attribute_statement.attribute:
                for val in attribute.attribute_value:
                    attributes['Role'].append(val.text)
        user = Users.map_saml(
            sender=current_app.name,
            subject=assertion.subject.name_id.text,
            attributes=attributes,
            assertion=assertion
        )
        registered_user = Database.session.query(Users).filter(Users.email == user.email).first()
        if registered_user:
            registered_user.assertion = user.assertion
        return registered_user

    @property
    def is_authenticated(self):
        if hasattr(self, "exp"):
            if getattr(self, 'exp'):
                logging.info("{}: exp '{}', now '{}' -> {} ".format(
                    __name__,
                    datetime.fromtimestamp(int(getattr(self, 'exp'))).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    datetime.fromtimestamp(
                        int(getattr(self, 'exp'))
                    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ") >= datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                ))
                return datetime.fromtimestamp(
                    int(getattr(self, 'exp'))
                ).strftime("%Y-%m-%dT%H:%M:%S.%fZ") >= datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if hasattr(self, "assertion"):
            if getattr(self, 'assertion'):
                logging.info("{}: exp '{}', now '{}' -> {} ".format(
                    __name__,
                    datetime.fromisoformat(
                        saml2.saml.assertion_from_string(getattr(self, 'assertion')).authn_statement[0]
                        .session_not_on_or_after
                    ).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    datetime.fromisoformat(
                        saml2.saml.assertion_from_string(getattr(self, 'assertion')).authn_statement[0]
                        .session_not_on_or_after
                    ).strftime('%Y-%m-%dT%H:%M:%S.%fZ') >= datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                ))
                return datetime.fromisoformat(
                    saml2.saml.assertion_from_string(getattr(self, 'assertion')).authn_statement[0]
                    .session_not_on_or_after
                ).strftime('%Y-%m-%dT%H:%M:%S.%fZ') >= datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return self.email is not None
