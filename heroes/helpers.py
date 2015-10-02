def admin_required(func):
    """Requires App Engine admin credentials.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.is_current_user_admin():
            raise exceptions.MethodNotAllowed('Admin credentials required.')
        return func(*args, **kwargs)
    return decorated_view


def get_enitity_by_key(key):
    return ndb.Key(urlsafe=key).get()
