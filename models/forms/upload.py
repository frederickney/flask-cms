# coding: utf-8


__author__ = 'Frederick NEY'

from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, StringField, HiddenField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    file = FileField(label='File', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Delete(FlaskForm):
    content = IntegerField(label='content', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Add(FlaskForm):
    file = FileField(label='File', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Plugin(FlaskForm):
    file = FileField(label='Plugin compressed file', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Process(FlaskForm):
    file = FileField(label='file', validators=[DataRequired()])
    ext = HiddenField(label='ext', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Content(FlaskForm):
    id = HiddenField(label='id')
    url = StringField(label='url', validators=[DataRequired()])
    name = StringField(label='Content name')
    content = StringField(label='Content')
    type = StringField(label='Content', validators=[DataRequired()])

    def __init__(self, id=None, url=None, name=None, content=None, type=None):
        super(Content, self).__init__()
        self.id.data = id,
        self.type.data = type
        self.url.data = url
        self.name.data = name
        self.content.data = content


class Restriction(FlaskForm):
    restricted_users = FieldList(label='Users')
    restricted_groups = FieldList(label='Groups')

    def __init__(self, retricted_users, restricted_goups):
        super(Restriction, self).__init__()
        self.restricted_users.type = StringField(label='User')
        self.restricted_users.data = retricted_users
        self.restricted_groups.type = StringField(label='Group')
        self.restricted_groups.data = restricted_goups


class Metadata(FlaskForm):
    title = StringField(label='Title')
    value = StringField(label='Value')


class Metadatas(FlaskForm):
    metas = FormField(Metadata, label='Metadatas')
