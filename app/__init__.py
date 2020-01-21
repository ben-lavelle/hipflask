from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging, os  # noqa: E401 (Ok to not use 'logging' here)
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'  # Name of login view

from app import routes, models, errors  # noqa: F401 (linting)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # INFO level logs for full issues
    file_handler = RotatingFileHandler('logs/hipflask.log',
                                       maxBytes=10240, backupCount=5)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('::: Hipflask starting :::')
