import re
import string

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
MAX_LENGTH_ORIGINAL = 2048
MAX_LENGTH_SHORT = 16
RESERVED_NAMES = {'files'}
ALLOWED_CHARS = string.ascii_letters + string.digits
ALLOWED_CHARS_PATTERN = re.compile(f'^[{ALLOWED_CHARS}]+$')

MESSAGES = {
    'missing_url_field': '"url" является обязательным полем!',
    'name_conflict': 'Предложенный вариант короткой ссылки уже существует.',
    'id_not_found': 'Указанный id не найден',
    'missing_body': 'Отсутствует тело запроса',
    'invalid_short_name': 'Указано недопустимое имя для короткой ссылки',
    'generation_error': 'Не удалось создать ссылку за {max_attempts} попыток',
    'upload_error': 'Ошибка при загрузке {file}: {error}',
    'error_download_link': 'Не удалось получить ссылку на скачивание',
    'server_error': 'Внутренняя ошибка сервера',
    'generic_error': 'Ошибка: {error}',
    'upload_url_error': 'Ошибка получения upload URL: {status}',
    'download_url_error': 'Ошибка получения download URL: {status}',
    'create': 'Создать',
    'load': 'Загрузить',
    'invalid_link_size': 'Недопустимый размер ссылки',
    'invalid_URL': 'Некорректный URL',
    'required_field': 'Обязательное поле'
}