import random
import string

from .models import URLMap


def get_unique_short_id(length=6, max_attempts=10):
    chars = string.ascii_letters + string.digits
    for _ in range(max_attempts):
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
    raise ValueError('Не удалось сгенерировать уникальный ID')
