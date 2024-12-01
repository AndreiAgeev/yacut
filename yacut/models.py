from datetime import datetime, timezone

from sqlalchemy.orm import validates

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now(timezone.utc)
    )

    @validates('short')
    def validate_short_link(self, key, short):
        from .utils import SHORT_LINK_LENGTH, validate_short
        if validate_short(short) or len(short) > SHORT_LINK_LENGTH:
            raise ValueError('Указано недопустимое имя для параметра short')
        return short

    def from_dict(self, data):
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self, url):
        return dict(
            url=self.original,
            short_link=url + self.short
        )
