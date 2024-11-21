from .finder import extract_fields
from flask_framework.Config import Environment

_mapper = {
    'email': ('email', str),
    'given_name': ('firstname', str),
    'family_name': ('lastname', str),
    'resource_access.{}.roles[admin]'.format(Environment.SERVER_DATA['APP_NAME']): ('is_admin', bool),
    'token': ('token', dict),
    'exp': ('exp', int)
}

openid = extract_fields(_mapper)
