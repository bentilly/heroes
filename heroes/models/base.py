from google.appengine.ext import ndb

from heroes import fields


def get_dbs(query, keys_only=None, **filters):
    model_class = ndb.Model._kind_map[query.kind]
    query_prev = query
    for prop, value in filters.iteritems():
        if value is None:
            continue
        for val in value if isinstance(value, list) else [value]:
            query = query.filter(model_class._properties[prop] == val)

    return list(query.fetch(keys_only=keys_only))


class Base(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    version = ndb.IntegerProperty(default=1)

    @classmethod
    def get_by(cls, name, value):
        return cls.query(getattr(cls, name) == value).get()

    @classmethod
    def get_dbs(cls, query=None, ancestor=None, limit=None, cursor=None, **kwargs):
        return get_dbs(query or cls.query(ancestor=ancestor), **kwargs)

    FIELDS = {
      'key': fields.Key,
      'id': fields.Id,
      'version': fields.Integer,
      'created': fields.DateTime,
      'modified': fields.DateTime}
