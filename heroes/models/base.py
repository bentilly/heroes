from uuid import uuid4

from google.appengine.ext import ndb


class BaseExpando(ndb.Expando):
    """Base class for heroes expando models.
    """
    revision = ndb.IntegerProperty(default=0)
    revision_created = ndb.DateProperty(auto_now_add=True)
    uid = ndb.StringProperty(required=True)
    latest = ndb.BooleanProperty(required=True, default=True)

    @classmethod
    def create_new_revision(cls, date=None, **kwargs):
        #XXX: make this transactional with "@ndb.transactional()" decorator.
        if not kwargs.get('uid'):
            # if not 'uid' provided - new model will be created
            kwargs['uid'] = str(uuid4())
            #TODO: get parent of last revision.

        # create new revision of model.
        new_entry = cls(**kwargs)

        # get latest revision of model based on uid.
        last_entry = cls.get_latest_revision(kwargs['uid'])
        if last_entry:
            # increment revision number.
            last_entry.latest = False
            last_entry.put()
            new_entry.revision = last_entry.revision + 1
            if date:
                new_entry.revision_created = date
        new_entry.put()
        return new_entry


    @classmethod
    def get_latest_revision(cls, uid):
        last_entry = cls.query(cls.uid == uid, cls.latest == True).fetch(limit=1)
        if last_entry:
            return last_entry[0]
        return None


    @classmethod
    def get_latest_revisions(cls, ancestor=None):
        entries_qry = cls.query(cls.latest == True, ancestor=ancestor)
        return entries_qry.fetch()


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
