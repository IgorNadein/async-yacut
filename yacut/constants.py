import re
import string

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
MAX_LENGTH_ORIGINAL = 2048
MAX_LENGTH_SHORT = 16
RESERVED_SHORT = {'files'}
ALLOWED_CHARS = string.ascii_letters + string.digits
ALLOWED_CHARS_PATTERN = re.compile(f'^[{re.escape(ALLOWED_CHARS)}]+$')
DEFAULT_SHORT_LENGTH = 6
MAX_GENERATION_ATTEMPTS = 10
REDIRECT_TO_URL_VIEW_NAME = 'redirect_to_url'
SWAGGER_URL = '/api/docs'
API_URL_DOCS = '/static/openapi.yml'


class Messages:
    MISSING_URL_FIELD = '"url" является обязательным полем!'
    NAME_CONFLICT = 'Предложенный вариант короткой ссылки уже существует.'
    ID_NOT_FOUND = 'Указанный id не найден'
    MISSING_BODY = 'Отсутствует тело запроса'
    INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
    GENERATION_ERROR = (
        f'Не удалось создать ссылку за '
        f'{MAX_GENERATION_ATTEMPTS} попыток'
    )
    UPLOAD_ERROR = 'Ошибка при загрузке {}: {}'
    ERROR_DOWNLOAD_LINK = 'Не удалось получить ссылку на скачивание'
    SERVER_ERROR = 'Внутренняя ошибка сервера'
    GENERIC_ERROR = 'Ошибка: {}'
    UPLOAD_URL_ERROR = 'Ошибка получения upload URL: {}'
    DOWNLOAD_URL_ERROR = 'Ошибка получения download URL: {}'
    CREATE = 'Создать'
    LOAD = 'Загрузить'
    INVALID_LINK_SIZE = 'Недопустимый размер ссылки'
    INVALID_URL = 'Некорректный URL'
    REQUIRED_FIELD = 'Обязательное поле'
