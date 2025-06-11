from http import HTTPStatus

from flask import jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

from . import app
from .constants import Messages
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import SWAGGER_URL, API_URL_DOCS


@app.route('/api/id/', methods=['POST'])
def create_short():
    data = request.get_json()
    if not data or 'url' not in data:
        raise InvalidAPIUsage(Messages.MISSING_URL_FIELD)
    try:
        original = data['url']
        return jsonify({
            'url': original,
            'short_link': URLMap.create(
                original=original,
                short=data.get('custom_id')
            ).get_short_url()
        }), HTTPStatus.CREATED
    except ValueError as message:
        raise InvalidAPIUsage(str(message))


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    url_map = URLMap.get_short(short=short)
    if not url_map:
        raise InvalidAPIUsage(
            Messages.ID_NOT_FOUND, HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})


app.register_blueprint(get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL_DOCS,
    config={'app_name': 'YaCut'}
), url_prefix=SWAGGER_URL)
