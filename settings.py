import os
from pathlib import Path


STATIC_PATH = Path(__file__).parent / 'html'


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
