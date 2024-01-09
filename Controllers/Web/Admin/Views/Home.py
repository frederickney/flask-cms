from flask_admin import AdminIndexView, expose
from flask_login import current_user, login_required


class Home(AdminIndexView):

    @login_required
    @expose('/')
    def index(self):
        from flask_framework import Extensions
        Extensions.load()
        return self.render('admin/home.html', exts=Extensions.all())
