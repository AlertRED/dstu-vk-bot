from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config.conf import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from web_app.admin import *
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.debug = True
    app.run()