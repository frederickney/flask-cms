# coding: utf-8


__author__ = 'Frederick NEY'

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField
from wtforms.validators import DataRequired


class CmsSettings(FlaskForm):
    Name = StringField(label='Settings name', validators=[DataRequired()])
    Value = StringField(label='Settings value', validators=[DataRequired()])
    submit = SubmitField(label='Create')


class CmsPluginsSettings(FlaskForm):
    Plugin = HiddenField(label='Plugin ID', validators=[DataRequired()])
    Name = StringField(label='Settings name', validators=[DataRequired()])
    Value = StringField(label='Settings Value', validators=[DataRequired()])
    submit = SubmitField(label='Create')


class CmsSettingsUpdate(FlaskForm):
    ID = HiddenField(label='Setting ID', validators=[DataRequired()])
    Value = StringField(validators=[DataRequired()])
    submit = SubmitField(label='Update')


class Delete(FlaskForm):
    ID = HiddenField(label='Setting ID', validators=[DataRequired()])
    submit = SubmitField(label='Delete')
