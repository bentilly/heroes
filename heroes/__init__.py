import os

from flask import Flask, g

from .users.controllers import users_bp
from .sports.controllers import sports_bp


def create_app():
    cur_dir = os.path.abspath(os.path.curdir)

    app = Flask(__name__,
                static_folder=os.path.join(cur_dir, 'static'),
                template_folder=os.path.join(cur_dir, 'static'))
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(sports_bp, url_prefix='/sports')

    app.config['DEBUG'] = True

    return app
