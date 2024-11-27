from flask import flash, redirect, render_template, request

from . import app, db
from .forms import ShortLinkForm
from .models import URLMap
from .utils import make_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = ShortLinkForm()
    if form.validate_on_submit():
        short_link = form.short_link.data
        if (
            short_link and
            URLMap.query.filter_by(short=short_link).first()
        ):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        elif not short_link:
            short_link = make_short_link()
        urlmap = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(urlmap)
        db.session.commit()
        short_link = request.url + short_link
        return render_template('index.html', form=form, short=short_link)
    return render_template('index.html', form=form)


@app.route('/<string:short_link>')
def short_link_redirect(short_link):
    urlmap = URLMap.query.filter_by(short=short_link).first()
    return redirect(urlmap.original)
