# coding: utf-8


__author__ = 'Frederick NEY'


from . import Ext
from .upload import Upload
from flask_framework.Server import deniedwebcall
from flask_admin.contrib import rediscli
from redis import Redis
from flask import Flask


@deniedwebcall
def setup():
    import flask_framework.Server as Server
    from flask_admin import Admin
    from . import Views
    adm = Admin(template_mode='bootstrap3', index_view=Views.Home())
    app: Flask = Server.Process.get()
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    adm.init_app(app)
    Server.Process._admin = adm
    load_views(adm, app)


@deniedwebcall
def load_views(adm, app):
    from flask_framework.Config import Environment
    """

    :param adm:
    :type adm: flask_admin.Admin
    :return:
    """

    """
        server.add_url_rule('/admin/', 'admin', Controllers.Web.Admin.Controller.index, methods=['GET'])
        server.add_url_rule('/admin/users/', 'admin.users', Controllers.Web.Admin.Controller.list_users, methods=['GET'])
        server.add_url_rule('/admin/setup/', 'admin.setup', Controllers.Web.Admin.Controller.setup, methods=['GET'])
        server.add_url_rule('/admin/plugins/', 'admin.plugins', Controllers.Web.Admin.Controller.setup, methods=['GET'])
        server.add_url_rule('/admin/plugins/add/', 'admin.plugins.upload', Controllers.Web.Admin.Controller.setup, methods=['GET'])
        server.add_url_rule('/admin/medias/', 'admin.medias', Controllers.Web.Admin.Controller.setup, methods=['GET'])
        server.add_url_rule('/admin/medias/add/', 'admin.medias.upload', Controllers.Web.Admin.Controller.setup, methods=['GET'])
        server.add_url_rule('/admin/pages/', 'admin.pages', Controllers.Web.Admin.Controller.setup, methods=['GET'])
        server.add_url_rule('/admin/pages/add/', 'admin.pages.add', Controllers.Web.Admin.Controller.setup, methods=['GET'])

        server.add_url_rule('/admin/upload/file/', 'admin.upload.file', Controllers.Web.Admin.Ext.UploadController.index, methods=['GET'])
        server.add_url_rule('/admin/upload/file/', 'admin.upload.send', Controllers.Web.Admin.Ext.UploadController.upload, methods=['POST'])
        server.add_url_rule('/admin/upload/process/', 'admin.upload.process', Controllers.Web.Admin.Ext.UploadController.process, methods=['POST'])
        server.add_url_rule('/admin/upload/success/', 'admin.upload.success', Controllers.Web.Admin.Ext.UploadController.success, methods=['GET'])

    """
    from . import Views
    adm.add_link(Views.Site())
    adm.add_view(Views.Plugins())
    adm.add_view(Views.Pages())
    adm.add_view(Views.Medias())
    adm.add_view(Views.Appearance())
    adm.add_view(Views.Settings())
    adm.add_sub_category('Users', 'Settings')
    app.register_blueprint(Views.Users().create_blueprint(adm))
    if 'redis' in Environment.Services:
        adm.add_views(rediscli.RedisCli(Redis(Environment.Services['redis']['HOST'], Environment.Services['redis']['PORT'])))
