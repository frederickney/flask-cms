from .finder import extract_fields

_mapper = {
    'subject': ('email', str),
    'attributes.Role[admin]': ('is_admin', bool),
    'assertion': ('assertion', str)
}

saml = extract_fields(_mapper)
