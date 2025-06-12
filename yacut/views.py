from flask import current_app, flash, redirect, render_template, request

from . import app
from .forms import FileUploadForm, URLMapForm
from .models import URLMap
from .ya_disk import upload_files_to_disk
from .constants import Messages


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    try:
        if not form.validate_on_submit():
            return render_template(
                'index.html',
                form=form,
            )
        return render_template(
            'index.html',
            form=form,
            url_map=URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data,
                form=form
            )
        )
    except Exception as e:
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
    return render_template(
        'files.html',
        form=form,
        results=zip(
            files, URLMap.batch_create(await upload_files_to_disk(files))
        )
    )
