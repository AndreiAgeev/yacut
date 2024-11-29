from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import FlaskConfig, STATIC_PATH


app = Flask(__name__, static_folder=STATIC_PATH, template_folder=STATIC_PATH)
app.config.from_object(FlaskConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, views
