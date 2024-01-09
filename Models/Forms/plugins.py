# coding: utf-8

__author__ = 'Frederick NEY'

from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, StringField, HiddenField
from wtforms.validators import DataRequired


class Enable(FlaskForm):

    Extension = HiddenField(label='Extension name', validators=[DataRequired()])
    submit = SubmitField(label='Enable')


class Delete(FlaskForm):

    Extension = HiddenField(label='Extension name', validators=[DataRequired()])
    submit = SubmitField(label='Delete')


class Disable(FlaskForm):

    Extension = HiddenField(label='Extension name', validators=[DataRequired()])
    submit = SubmitField(label='Disable')
