from flask_admin.menu import MenuLink


class Site(MenuLink):

    def __init__(self):
        super(Site, self).__init__('Back to site', endpoint='home')
