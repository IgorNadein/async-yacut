from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db
from .constants import Messages
from .exceptions import InvalidAPIUsage


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
        'message': Messages.MISSING_BODY,
    }), HTTPStatus.BAD_REQUEST


@app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
def handle_unsupported_media_type(error):
    return jsonify({
        'message': Messages.MISSING_BODY,
    }), HTTPStatus.BAD_REQUEST
