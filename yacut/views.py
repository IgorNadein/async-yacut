from flask import flash, redirect, render_template, request
from sqlalchemy.exc import IntegrityError

from . import app, db
from .forms import FileUploadForm, URLMapForm
from .models import URLMap
from .utils import get_unique_short_id
from .ya_disk import upload_to_disk


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    short_url = request.args.get('short')
    if form.validate_on_submit():
        original_url = form.original_link.data
        custom_id = (form.custom_id.data.strip()
                     if form.custom_id.data else None)

        try:
            if not custom_id:
                custom_id = get_unique_short_id()

            url_map = URLMap(
                original=original_url,
                short=custom_id
            )
            db.session.add(url_map)
            db.session.commit()

            return render_template(
                'index.html',
                form=form,
                short_url=custom_id
            ), 200

        except IntegrityError:
            db.session.rollback()
            flash('Произошла ошибка при создании ссылки', 'danger')
            return render_template('index.html', form=form)
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Ошибка: {str(e)}')
            flash('Внутренняя ошибка сервера', 'danger')
            return render_template('index.html', form=form)

    return render_template(
        'index.html',
        form=form,
        short_url=short_url
    )


@app.route('/<short_id>')
def redirect_to_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
async def files():
    form = FileUploadForm()
    if form.validate_on_submit():
        files = request.files.getlist('files')
        results = []

        for file in files:
            try:
                short_id = get_unique_short_id()

                download_url = await upload_to_disk(file)
                if not download_url:
                    raise Exception("Не удалось получить ссылку на скачивание")
                url_map = URLMap(
                    original=download_url,
                    short=short_id,
                )
                db.session.add(url_map)

                results.append({
                    'name': file.filename,
                    'url': short_id,
                    'download_url': download_url
                })

            except Exception as e:
                flash(
                    f'Ошибка при загрузке {file.filename}: {str(e)}', 'danger')

        db.session.commit()
        return render_template('files.html', form=form, results=results)

    return render_template('files.html', form=form)