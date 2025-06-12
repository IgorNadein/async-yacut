from flask import current_app, flash, redirect, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint

from . import app
from .constants import API_URL_DOCS, SWAGGER_URL, Messages
from .exceptions import DiskUploadError
from .forms import FileUploadForm, URLMapForm
from .models import URLMap
from .ya_disk import upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(
            'index.html',
            form=form,
        )
    try:
        return render_template(
            'index.html',
            form=form,
            url_map=URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data,
                validate=True
            )
        )
    except (ValueError, URLMap.ShortGenerationError) as e:
        current_app.logger.error(Messages.GENERIC_ERROR.format(e))
        flash(Messages.SERVER_ERROR, 'danger')
        return render_template(
            'index.html',
            form=form
        )


@app.route('/<short>')
def redirect_to_url(short):
    return redirect(URLMap.get_short_or_404(short=short).original)


@app.route('/files', methods=['GET', 'POST'])
async def files():
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = request.files.getlist('files')
    try:
        return render_template(
            'files.html',
            form=form,
            results=zip(
                files,
                URLMap.batch_create(await upload_files_to_disk(files))
            )
        )
    except (ValueError, URLMap.ShortGenerationError, DiskUploadError) as e:
        current_app.logger.error(Messages.GENERIC_ERROR.format(e))
        flash(Messages.SERVER_ERROR, 'danger')
        return render_template(
            'index.html',
            form=form
        )

app.register_blueprint(get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL_DOCS,
    config={'app_name': 'YaCut'}
), url_prefix=SWAGGER_URL)