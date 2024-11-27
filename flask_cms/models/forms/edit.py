# coding: utf-8


__author__ = 'Frederick NEY'

from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, TextAreaField, StringField, FieldList, BooleanField, FormField, IntegerField, SelectField
from wtforms.widgets import HiddenInput

from wtforms.validators import DataRequired, InputRequired, Optional


class Form(FlaskForm):
    content = HiddenField(label='content', validators=[InputRequired()])
    submit = SubmitField(label='submit')


class Meta(FlaskForm):
    key = StringField(label='key')
    value = TextAreaField(label='value')


class NewContent(FlaskForm):
    content = TextAreaField(label='content', validators=[DataRequired(), InputRequired()])
    metas = FieldList(FormField(Meta), label='metadata')
    title = StringField(label='title', validators=[DataRequired(), InputRequired()])
    url = StringField(label='url', validators=[DataRequired(), InputRequired()])
    publish = BooleanField(label='published')
    type = HiddenField(label='type', validators=[DataRequired(), InputRequired()])
    parent = SelectField(label='parent', validators=[Optional()])
    submit = SubmitField(label='submit')

class Content(FlaskForm):
    content = TextAreaField(label='content', validators=[DataRequired(), InputRequired()])
    metas = FieldList(FormField(Meta), label='metadata')
    title = StringField(label='title', validators=[DataRequired(), InputRequired()])
    url = StringField(label='url', validators=[DataRequired(), InputRequired()])
    publish = BooleanField(label='published')
    type = HiddenField(label='type', validators=[DataRequired(), InputRequired()])
    submit = SubmitField(label='submit')
    parent = SelectField(label='parent', validators=[Optional()])
    id = IntegerField(label='id', widget=HiddenInput())

