# coding: utf-8


__author__ = 'Frederick NEY'


from flask_wtf import FlaskForm, Form
from wtforms import SubmitField, HiddenField, TextAreaField, StringField, FieldList, BooleanField, FormField
from wtforms.validators import DataRequired, InputRequired


class Form(FlaskForm):

    content = HiddenField(label='content', validators=[InputRequired()])
    submit = SubmitField(label='submit')


class Meta(FlaskForm):
    key = StringField(label='key')
    value = TextAreaField(label='value')


class Content(FlaskForm):
    content = TextAreaField(label='content')
    metas = FieldList(FormField(Meta), label='metadata')
    title = StringField(label='title')
    url = StringField(label='url')
    publish = BooleanField(label='published')
    type = HiddenField(label='type', validators=[DataRequired(), InputRequired()])
    submit = SubmitField(label='submit')