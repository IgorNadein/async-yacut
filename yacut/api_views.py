from flask import jsonify, request, url_for
from wtforms.validators import ValidationError

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from .validators import validate_custom_id


@app.route('/api/id/', methods=['POST'])
def create_short_url():

    data = request.get_json()
    if not data or 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    try:
        validate_custom_id(custom_id)
    except ValidationError as message:
        raise InvalidAPIUsage(str(message), 400)

    url_map = URLMap(
        original=data['url'],
        short=custom_id or get_unique_short_id()
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_to_url',
            short_id=url_map.short,
            _external=True
        )
    }), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
