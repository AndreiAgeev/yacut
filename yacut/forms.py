from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, ValidationError, URL
)

from .utils import CHARSET


ERROR_MESSAGE = (
    'Присутствуют неподхоящие символы. Разрешены только '
    'латинские символы верхнего и нижнего регистра, и цифры')


class ShortLinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message='Некорректный URL')
        )
    )
    short_link = StringField(
        'Ваш вариант короткой ссылки',
        validators=(Length(1, 16), Optional())
    )
    submit = SubmitField('Создать')

    def validate_short_link(form, field):
        for letter in list(field.data):
            if letter not in CHARSET:
                raise ValidationError(ERROR_MESSAGE)
