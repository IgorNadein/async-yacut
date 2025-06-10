# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired

from .validators import custom_id_validator_wtf


class URLMapForm(FlaskForm):
    original_link = StringField(
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(require_tld=True, message='Некорректный URL')
        ]
    )
    custom_id = StringField(
        validators=[custom_id_validator_wtf]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField()

    submit = SubmitField('Загрузить')
