from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, ValidationError, URL
)

from .utils import SHORT_LINK_LENGTH, validate_short


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
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(Length(1, SHORT_LINK_LENGTH), Optional())
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        if validate_short(field.data):
            raise ValidationError(ERROR_MESSAGE)
