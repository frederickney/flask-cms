# coding: utf-8


__author__ = 'Frederick NEY'

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    theme = SelectField(label='theme', validators=[DataRequired()])
    submit = SubmitField(label='submit')
