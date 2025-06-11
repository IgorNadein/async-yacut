from flask import redirect, render_template, request

from . import app
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
    return render_template(
        'index.html',
        form=form,
        url_map=URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data
        )
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
    results = URLMap.batch_create(await upload_files_to_disk(files))
    return render_template('files.html', form=form, results=results)
