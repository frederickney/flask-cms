from flask_admin import BaseView, expose


class Setup(BaseView):



    @expose('/')
    def index(self):
        return self.render('admin/setup.html')

