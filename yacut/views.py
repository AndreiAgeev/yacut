from flask import flash, redirect, render_template, request

from . import app, db
from .forms import ShortLinkForm
from .models import URLMap
from .utils import make_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = ShortLinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if (
        custom_id and
        URLMap.query.filter_by(short=custom_id).first()
    ):
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)
    elif not custom_id:
        custom_id = make_short_link()
    urlmap = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return render_template(
        'index.html',
        form=form,
        short=request.host_url + custom_id
    )


@app.route('/<string:custom_id>')
def short_link_redirect(custom_id):
    urlmap = URLMap.query.filter_by(short=custom_id).first_or_404()
    return redirect(urlmap.original)
