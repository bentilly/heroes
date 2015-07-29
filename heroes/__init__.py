import os

from flask import Flask

from .users.controllers import users_bp


def create_app():
    cur_dir = os.path.abspath(os.path.curdir)

    app = Flask(__name__,
                static_folder=os.path.join(cur_dir, 'static'),
                template_folder=os.path.join(cur_dir, 'static'))
    app.register_blueprint(users_bp, url_prefix='/users')

    app.config['DEBUG'] = True

    return app
