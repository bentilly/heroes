from flask import Blueprint, session, jsonify

from google.appengine.api import users


users_bp = Blueprint('users', __name__)

@users_bp.route('/config/')
def user_config():
    user = users.get_current_user()
    data = {'user_id': '', 'is_admin': False}
    if user:
        data['user_id'] = user.user_id()
        if users.is_current_user_admin():
            data['is_admin'] = True
    else:
        data['login_url'] = users.create_login_url('/')
        data['logout_url'] = users.create_logout_url('/')
    return jsonify(data)
