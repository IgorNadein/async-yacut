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


class ShortIDGenerationError(RuntimeError):
    """Кастомное исключение для ошибок генерации коротких ссылок"""
    pass


class FileUploadError(RuntimeError):
    """Кастомное исключение для ошибок загрузки файлов"""
    pass
