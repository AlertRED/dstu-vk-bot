from flask import Flask
from config.conf import Config

flask_app = Flask(__name__)
flask_app.config.from_object(Config)

from app.models import models_DB
from web_app.routes import *

if __name__ == '__main__':
    flask_app.run()