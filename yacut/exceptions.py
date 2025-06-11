from http import HTTPStatus


class DiskUploadError(Exception):
    """Базовое исключение для ошибок загрузки"""

    def __init__(
            self,
            message,
            status_code=None,
            url=None
    ):
        self.status_code = status_code
        self.url = url
        super().__init__(message)


class ShortIDGenerationError(Exception):
    """Кастомное исключение для ошибок генерации коротких ссылок"""


class FileUploadError(Exception):
    """Кастомное исключение для ошибок загрузки файлов"""


class InvalidAPIUsage(Exception):
    """Исключение для API"""
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
