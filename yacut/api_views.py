from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import Messages
from .exceptions import InvalidAPIUsage
from .models import URLMap


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
    except (ValueError, URLMap.ShortGenerationError) as e:
        raise InvalidAPIUsage(str(e))


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    url_map = URLMap.get(short=short)
    if not url_map:
        raise InvalidAPIUsage(
            Messages.ID_NOT_FOUND, HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})
