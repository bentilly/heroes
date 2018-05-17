import os

from flask import Flask, g

from .sports.controllers import sports_bp
from .countries.controllers import country_bp
from .divisions.controllers import division_bp
from .roles.controllers import role_bp
from .positions.controllers import position_bp
from .teams.controllers import team_bp
from .events.controllers import event_bp
from .squads.controllers import squad_bp
from .representatives.controllers import rep_bp
from .squadmembers.controllers import squadmember_bp
from .venues.controllers import venue_bp
from .matches.controllers import match_bp
from .matchteams.controllers import matchteam_bp
from .matchteammembers.controllers import matchteammember_bp
from .trophies.controllers import trophy_bp
from .images.controllers import image_bp

# public web pages
from .heroesweb.controllers import heroesweb_bp


import config


def create_app():
    cur_dir = os.path.abspath(os.path.curdir)

    app = Flask(__name__,
                static_folder=os.path.join(cur_dir, 'static'),
                template_folder=os.path.join(cur_dir, 'templates'))
    app.register_blueprint(sports_bp, url_prefix='/admin/sport')
    #NEXT sports/controllers.py
    app.register_blueprint(country_bp, url_prefix='/admin/country')
    app.register_blueprint(division_bp, url_prefix='/admin/division')
    app.register_blueprint(role_bp, url_prefix='/admin/role')
    app.register_blueprint(position_bp, url_prefix='/admin/position')
    app.register_blueprint(team_bp, url_prefix='/admin/team')
    app.register_blueprint(event_bp, url_prefix='/admin/event')
    app.register_blueprint(squad_bp, url_prefix='/admin/squad')
    app.register_blueprint(rep_bp, url_prefix='/admin/rep')
    app.register_blueprint(squadmember_bp, url_prefix='/admin/squadmember')
    app.register_blueprint(venue_bp, url_prefix='/admin/venue')
    app.register_blueprint(match_bp, url_prefix='/admin/match')
    app.register_blueprint(matchteam_bp, url_prefix='/admin/matchteam')
    app.register_blueprint(matchteammember_bp, url_prefix='/admin/matchteammember')
    app.register_blueprint(trophy_bp, url_prefix='/admin/trophy')
    app.register_blueprint(image_bp, url_prefix='/image')

    # public web pages
    app.register_blueprint(heroesweb_bp, url_prefix='/')
    #NEXT heroes/heroesweb/controllers.py

    return app
