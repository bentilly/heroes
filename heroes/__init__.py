import os

from flask import Flask, g

from .sports.controllers import sports_bp


import config


def create_app():
    cur_dir = os.path.abspath(os.path.curdir)

    app = Flask(__name__,
                static_folder=os.path.join(cur_dir, 'static'),
                template_folder=os.path.join(cur_dir, 'templates'))
    app.register_blueprint(sports_bp, url_prefix='/sports')



    return app
