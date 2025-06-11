# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .constants import (ALLOWED_CHARS_PATTERN, MAX_LENGTH_ORIGINAL,
                        MAX_LENGTH_SHORT, Messages)
from .models import URLMap


class URLMapForm(FlaskForm):
    original_link = StringField(
        validators=[
            DataRequired(message=Messages.REQUIRED_FIELD),
            URL(require_tld=True, message=Messages.INVALID_URL),
            Length(
                max=MAX_LENGTH_ORIGINAL,
                message=Messages.INVALID_LINK_SIZE
            )
        ]
    )
    custom_id = StringField(
        validators=[
            Optional(),
            Length(
                max=MAX_LENGTH_SHORT,
                message=Messages.INVALID_LINK_SIZE
            ),
            Regexp(
                ALLOWED_CHARS_PATTERN,
                message=Messages.INVALID_SHORT_NAME
            )
        ]
    )
    submit = SubmitField(Messages.CREATE)

    def validate_custom_id(self, field):
        try:
            URLMap.validate_short(
                short=field.data,
                check_length=False,
                check_chars=False,
            )
        except ValueError as e:
            raise ValidationError(str(e))


class FileUploadForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField(Messages.LOAD)
