from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import MESSAGES
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short():

    data = request.get_json()
    model = URLMap()
    if not data or 'url' not in data:
        raise InvalidAPIUsage(MESSAGES['missing_url_field'])

    short = data.get('custom_id')
    try:
        url_map = model.create(
            original=data['url'],
            short=short
        )
        return jsonify({
            'url': url_map.original,
            'short_link': url_map.get_short()
        }), HTTPStatus.CREATED
    except ValueError as message:
        raise InvalidAPIUsage(str(message))


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if not url_map:
        raise InvalidAPIUsage(
            MESSAGES['id_not_found'], HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})
