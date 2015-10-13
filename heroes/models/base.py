from google.appengine.ext import ndb


class BaseExpando(ndb.Expando):
    """Base class for heroes expando models.
    """
    revision = ndb.IntegerProperty(default=0)


class Base(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    version = ndb.IntegerProperty(default=1)


    class Meta:
        def __init__(self):
	    self.fields = []


    @property
    def admin_fields(self):
        from ndbadmin.admin import fields
        return fields


    @classmethod
    def get_by(cls, name, value):
        return cls.query(getattr(cls, name) == value).get()


    @property
    def link(self):
        return '/{}s/{}/'.format(self.__class__.__name__.lower(), self.key.urlsafe())
