from flask_admin import BaseView, expose
from flask_login import login_required


class Users(BaseView):

    def __init__(self):
        super(Users, self).__init__()

    @login_required
    @expose('/')
    def index(self):
        return self.render('admin/setup.html')


