import random
from datetime import datetime, timezone

from flask import abort, url_for

from . import app, db
from .constants import (ALLOWED_CHARS, ALLOWED_CHARS_PATTERN, MESSAGES,
                        MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT, RESERVED_NAMES)
from .exceptions import ShortIDGenerationError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime,
                          default=lambda: datetime.now(timezone.utc))

    @classmethod
    def validate_short(cls, short):
        """Централизованная валидация короткой ссылки"""
        if len(short) > MAX_LENGTH_SHORT or not ALLOWED_CHARS_PATTERN.match(
            short
        ):
            raise ValueError(MESSAGES['invalid_short_name'])
        if short in RESERVED_NAMES or cls.get(short=short):
            raise ValueError(
                MESSAGES['name_conflict']
            )

    @classmethod
    def create(cls, original, short=None):
        if not short:
            short = cls.get_unique_short()
        cls.validate_short(short)
        new_url = cls(original=original, short=short)
        db.session.add(new_url)
        db.session.commit()
        return new_url

    @classmethod
    def get(cls, short=None, original=None):
        if short:
            return cls.query.filter_by(short=short).first()
        if original:
            return cls.query.filter_by(original=original).first()
        return None

    @classmethod
    def get_or_404(cls, short):
        url_map = cls.get(short=short)
        if not url_map:
            abort(404, description=MESSAGES['id_not_found'])
        return url_map

    @classmethod
    def get_unique_short(cls, length=6, max_attempts=10):
        for _ in range(max_attempts):
            short = ''.join(random.choices(ALLOWED_CHARS, k=length))
            if not cls.get(short=short):
                return short
        raise ShortIDGenerationError(
            MESSAGES['generation_error'].format(max_attempts)
        )

    def get_short(self):
        return url_for(
            app.config['REDIRECT_TO_URL_VIEW_NAME'],
            short=self.short,
            _external=True
        )
