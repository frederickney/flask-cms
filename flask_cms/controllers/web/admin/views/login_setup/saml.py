# coding: utf-8

from flask_admin import expose
from flask_framework.Server import Process
from flask_framework.Utils.Auth import admin_login_required as login_required

from flask_cms.views import BaseView


class Login(BaseView):

    def __init__(self):
        super(Login, self).__init__(endpoint='admin:login:saml2', url='/admin/saml2/')
        Process.login_manager().blueprint_login_views.update({'admin:login:saml2': "admin:login.index"})
        Process._csrf.exempt("{}.authorize".format(__name__))
        Process._csrf.exempt("{}.logout".format(__name__))

    @expose('/', methods=['GET'])
    def index(self):
        return Process.saml.saml_login(prefix='admin:login:saml2')

    @expose('/login/', methods=['GET'])
    def login(self):
        return Process.saml.saml_login(prefix='admin:login:saml2')

    @expose('/metadata/', methods=['GET'])
    def metadata(self):
        return Process.saml.metadata(prefix='admin:login:saml2')

    @expose('/authorize/', methods=['POST'])
    def authorize(self):
        return Process.saml.authorize(prefix='admin:login:saml2')

    @login_required
    @expose('/logout/', methods=['POST', 'GET'])
    def logout(self):
        return Process.saml.saml_logout()

    @staticmethod
    def user(id):
        return Process.openid.user(id)
