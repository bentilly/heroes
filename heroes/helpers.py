from google.appengine.api import images
from google.appengine.ext import ndb


def admin_required(func):
    """Requires App Engine admin credentials.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.is_current_user_admin():
            raise exceptions.MethodNotAllowed('Admin credentials required.')
        return func(*args, **kwargs)
    return decorated_view


def get_entity_by_key(key):
    return ndb.Key(urlsafe=key).get()


def get_image_url(entry_key, attr_name):
    return '/image/{}/{}/'.format(entry_key, attr_name)
