from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db
from .constants import MESSAGES


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify({'message': error.message}), error.status_code


@app.errorhandler(HTTPStatus.BAD_REQUEST)
def page_not_found(error):
    return render_template('errors/404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(HTTPStatus.BAD_REQUEST)
def handle_bad_request(error):
    return jsonify({
        'message': MESSAGES['missing_body'],
    }), HTTPStatus.BAD_REQUEST


@app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
def handle_unsupported_media_type(error):
    return jsonify({
        'message': MESSAGES['missing_body'],
    }), HTTPStatus.BAD_REQUEST
