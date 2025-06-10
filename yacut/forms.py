# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length, ValidationError

from .constants import MESSAGES, MAX_LENGTH_ORIGINAL
from .models import URLMap


class URLMapForm(FlaskForm):
    original_link = StringField(
        validators=[
            DataRequired(message=MESSAGES['required_field']),
            URL(require_tld=True, message=MESSAGES['invalid_URL']),
            Length(
                max=MAX_LENGTH_ORIGINAL,
                message=MESSAGES['invalid_link_size']
            )
        ]
    )
    custom_id = StringField(
        validators=[]
    )
    submit = SubmitField(MESSAGES['create'])

    def validate_custom_id(self, field):
        """Кастомный валидатор, интегрирующий проверки из модели"""
        if field.data:
            try:
                URLMap.validate_short(field.data)
            except ValueError as e:
                raise ValidationError(str(e))


class FileUploadForm(FlaskForm):
    files = MultipleFileField()

    submit = SubmitField(MESSAGES['load'])
