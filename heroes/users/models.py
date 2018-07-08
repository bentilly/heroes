from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Editor(Base):
	userid = ndb.StringProperty(required=True)
	firstname = ndb.StringProperty()
	lastname = ndb.StringProperty()
	phone = ndb.StringProperty()
	country = ndb.StringProperty()
	sport = ndb.StringProperty()

