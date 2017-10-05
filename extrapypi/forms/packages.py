"""Forms for packages

Used for dashboard and standard upload
"""
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import StringField, TextAreaField, FieldList


class UploadForm(FlaskForm):
    action = StringField(':action', validators=[validators.required()])
    name = StringField('name', validators=[validators.required()])
    summary = StringField('summary')
    description = TextAreaField(
        'description',
        validators=[validators.optional()]
    )
    download_url = URLField('download_url', validators=[validators.optional()])
    home_page = URLField('home_page', validators=[validators.optional()])
    version = StringField('version', validators=[validators.required()])
    keywords = FieldList(StringField('keywords'))
    md5_digest = StringField('md5_digest', validators=[validators.required()])

    class Meta:
        csrf = False
