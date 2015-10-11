"""Trophies-related controllers.
"""
from flask import Blueprint, render_template, redirect, request

from .models import Trophie

trophie_bp = Blueprint('trophie', __name__)


@trophie_bp.route('/new/')
@trophie_bp.route('/new/<sport_key>/')
def new_trophie(sport_key=None):
    if sport_key is not None:
        pass
    return render_template('trophie.html')


@trophie_bp.route('/<key>')
def read_trophie():
    pass


@trophie_bp.route('/<key>')
def update_trophie():
    pass


@trophie_bp.route('/<key>')
def delete_trophie():
    pass
