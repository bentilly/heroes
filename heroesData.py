
from google.appengine.ext import ndb

class Sport(ndb.Model):
	title = ndb.StringProperty(indexed=False)
	description = ndb.StringProperty(indexed=False)
