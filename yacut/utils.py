from random import randint, sample
from string import ascii_letters, digits

from .models import URLMap


CHARSET = ascii_letters + digits


# def encode62(digit):
#     """Преобразовывает полученное число digit в строку base62."""
#     a = []
#     while digit:
#         digit, r = divmod(digit, 62)
#         a.insert(0, CHARSET[r])
#     if not a:
#         return CHARSET[0]
#     return ''.join(a)


def make_short_link():
    """
    Создаёт короткую ссылку для сохранённой в БД полной ссылки.
    Изначально ссылка создаётся из id записи в БД с помощью функции encode62().
    В ситуации, если такая короткая ссылка уже присутствует в БД, то
    формируем её методом с помщью функции sample библиотеки random.
    Длина такой ссылки - 10-16 символов (меньше вероятность получить дубликат).
    """
    while True:
        short_link = ''.join(sample(CHARSET, k=randint(6, 16)))
        if not URLMap.query.filter_by(short=short_link).first():
            break
    return short_link
