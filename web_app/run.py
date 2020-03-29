from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.conf import Config

flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db = SQLAlchemy(flask_app)

from app.models import models_DB
from web_app.routes import *

if __name__ == '__main__':
    flask_app.run()