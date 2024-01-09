from flask_admin import BaseView, expose
from flask_login import login_required


class Pages(BaseView):

    def __init__(self):
        super(Pages, self).__init__(endpoint='admin#pages', url='/admin/pages/')

    @expose('/')
    @login_required
    def index(self):
        from Models.Persistent.cms import Contents
        return self.render('admin/setup.html')

    @expose('/add/', methods=['GET'])
    @login_required
    def add(self):
        from Models.Forms.upload import Content
        return self.render('admin/upload/index.html', form=Content)

    @expose('/save/', methods=['POST'])
    @login_required
    def save(self):
        pass

    @expose('/delete/', methods=['POST'])
    @login_required
    def delete(self):
        pass