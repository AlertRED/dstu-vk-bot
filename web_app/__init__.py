from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config.conf import Config

flask_app = Flask(__name__)
flask_app.config.from_object(Config)

# db = SQLAlchemy(flask_app, engine_options={'pool_size': 10, 'max_overflow': 2})
db = SQLAlchemy(flask_app)

@flask_app.route('/')
def hello_world():
    return redirect('/admin')\

@flask_app.route('/test')
def test():
    return 'test'

if __name__ == '__main__':
    from web_app.admin import *

    migrate = Migrate(flask_app, db)
    flask_app.debug = False
    flask_app.run()
