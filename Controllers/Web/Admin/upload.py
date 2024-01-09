
from flask_admin.menu import MenuLink


class Upload(MenuLink):

    def __init__(self, parent):
        super(Upload, self).__init__("Upload", endpoint='admin#%s#upload' % parent.split('.')[-1].lower(), category=parent.split('.')[-1])