from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config.conf import Config

flask_app = Flask(__name__)

flask_app.config.from_object(Config)
db = SQLAlchemy(flask_app)

import web_app.admin

if __name__ == '__main__':
    migrate = Migrate(flask_app, db)
    flask_app.run()
