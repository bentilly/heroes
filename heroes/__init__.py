import os

from flask import Flask, g

from werkzeug.wsgi import DispatcherMiddleware

from .users.controllers import users_bp
from .sports.controllers import sports_bp

import config


def create_app():
    cur_dir = os.path.abspath(os.path.curdir)

    app = Flask(__name__,
                static_folder=os.path.join(cur_dir, 'static'),
                template_folder=os.path.join(cur_dir, 'templates'))
    app.config.from_object(config)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(sports_bp, url_prefix='/sports')

    if app.config.get('ADMIN_ENABLED'):
        app = enable_admin_app(app)

    return app


def enable_admin_app(app):
    # from ndbadmin.main import app as ndbadmin_app
    return DispatcherMiddleware(DispatcherMiddleware(app, {
        '/admin': app
    })
