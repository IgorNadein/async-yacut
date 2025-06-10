import re

from wtforms.validators import ValidationError

from .models import URLMap

RESERVED_NAMES = {'files', 'api'}
ALLOWED_CHARS = re.compile(r'^[A-Za-z0-9]+$')
MAX_LENGTH = 16


def validate_custom_id(custom_id: str) -> None:
    """Универсальная валидация короткой ссылки."""
    if not custom_id:
        return
    if custom_id in RESERVED_NAMES or URLMap.query.filter_by(
        short=custom_id
    ).first():
        raise ValidationError(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if len(custom_id) > MAX_LENGTH or not ALLOWED_CHARS.match(custom_id):
        raise ValidationError('Указано недопустимое имя для короткой ссылки')


def custom_id_validator_wtf(form, field):
    """Адаптер для интеграции с WTForms"""
    validate_custom_id(field.data)
