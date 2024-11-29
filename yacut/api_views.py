from flask import jsonify, request

from . import app, db
from .error_handlers import APIException
from .models import URLMap
from .utils import make_short_link, validate_short


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise APIException('Отсутствует тело запроса')
    elif 'url' not in data:
        raise APIException('"url" является обязательным полем!')
    if 'custom_id' in data and (
        validate_short(data['custom_id']) or
        len(data['custom_id']) > 16
    ):
        raise APIException('Указано недопустимое имя для короткой ссылки')
    elif (
        'custom_id' in data and
        URLMap.query.filter_by(short=data['custom_id']).first()
    ):
        raise APIException(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    elif 'custom_id' not in data:
        data['custom_id'] = make_short_link()
    urlmap = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict(request.host_url)), 201


@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_url(short_link):
    urlmap = URLMap.query.filter_by(short=short_link).first()
    if not urlmap:
        raise APIException('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original}), 200
