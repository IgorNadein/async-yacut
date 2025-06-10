from flask import redirect, render_template, request

from . import app
from .forms import FileUploadForm, URLMapForm
from .models import URLMap
from .ya_disk import upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    model = URLMap()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template(
            'index.html',
            form=form,
        )

    original_url = form.original_link.data
    short = (form.custom_id.data.strip()
             if form.custom_id.data else None)

    url_map = model.create(
        original=original_url,
        short=short
    )
    return render_template(
        'index.html',
        form=form,
        url_map=url_map
    )


@app.route('/<short>')
def redirect_to_url(short):
    url_map = URLMap.get_or_404(short=short)
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
async def files():
    form = FileUploadForm()
    model = URLMap()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = request.files.getlist('files')
    results = []
    download_urls = await upload_files_to_disk(files)
    for filename, url in download_urls:
        url_map = model.create(
            original=url,
        )
        results.append({
            'name': filename,
            'url_map': url_map,
            'download_url': url
        })

    return render_template('files.html', form=form, results=results)
