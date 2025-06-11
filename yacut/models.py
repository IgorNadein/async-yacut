import random
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import url_for

from . import db
from .constants import (ALLOWED_CHARS, ALLOWED_CHARS_PATTERN,
                        DEFAULT_SHORT_LENGTH, MAX_GENERATION_ATTEMPTS,
                        MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT,
                        REDIRECT_TO_URL_VIEW_NAME, RESERVED_SHORT, Messages)
from .exceptions import ShortIDGenerationError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime,
                          default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def validate_short(
        short: str,
        check_length: bool = True,
        check_chars: bool = True,
        check_reserved: bool = True,
        check_existence: bool = True
    ):
        """
        Централизованная валидация короткой ссылки
        с возможностью отключения проверок.
        """

        if check_length and (len(short) > MAX_LENGTH_SHORT):
            raise ValueError(Messages.INVALID_SHORT_NAME)

        if check_chars and not ALLOWED_CHARS_PATTERN.match(short):
            raise ValueError(Messages.INVALID_SHORT_NAME)

        if check_reserved and short in RESERVED_SHORT:
            raise ValueError(Messages.NAME_CONFLICT)

        if check_existence and URLMap.get_short(short=short):
            raise ValueError(Messages.NAME_CONFLICT)

    @staticmethod
    def validate_original(original):
        """Централизованная валидация ссылок"""
        if len(original) > MAX_LENGTH_ORIGINAL:
            raise ValueError(Messages.INVALID_LINK_SIZE)
        parsed = urlparse(original)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(Messages.INVALID_URL)
        if parsed.scheme not in ('http', 'https'):
            raise ValueError(Messages.INVALID_URL)

    @staticmethod
    def create(original, short=None):
        URLMap.validate_original(original)
        if not short:
            short = URLMap.get_unique_short()
        else:
            URLMap.validate_short(short)
        new_url = URLMap(original=original, short=short)
        db.session.add(new_url)
        db.session.commit()
        return new_url

    @staticmethod
    def get_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_short_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404(
            description=Messages.ID_NOT_FOUND
        )

    @staticmethod
    def get_unique_short():
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(
                    ALLOWED_CHARS,
                    k=DEFAULT_SHORT_LENGTH
                )
            )
            if not URLMap.get_short(short=short):
                return short
        raise ShortIDGenerationError(
            Messages.GENERATION_ERROR
        )

    @staticmethod
    def batch_create(urls):
        return [{
            'name': filename,
            'url_map': URLMap.create(original=url),
            'download_url': url
        } for filename, url in urls
        ]

    def get_short_url(self):
        return url_for(
            REDIRECT_TO_URL_VIEW_NAME,
            short=self.short,
            _external=True
        )
