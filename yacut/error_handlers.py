from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify({'message': error.message}), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        "message": 'Отсутствует тело запроса',
    }), 400


@app.errorhandler(415)
def handle_unsupported_media_type(error):
    return jsonify({
        "message": "Отсутствует тело запроса",
    }), 400