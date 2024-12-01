from random import choices
from string import ascii_letters, digits

from .models import URLMap


CHARSET = ascii_letters + digits
SHORT_LINK_LENGTH = 16
RANDOM_SHORT_LINK_LENGTH = 6


def make_short_link():
    while True:
        short_link = ''.join(choices(CHARSET, k=RANDOM_SHORT_LINK_LENGTH))
        if not URLMap.query.filter_by(short=short_link).first():
            break
    return short_link


def validate_short(short):
    for letter in list(short):
        if letter not in CHARSET:
            return True
