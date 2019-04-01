from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

#Basic holder for the HTML used in a template. 
# CSS, images and other resources stored as files in Cloudstorage
# PARENT is the object that will use this template (eg: COUNTRY will have several child templates)
class Template(Base):
	content = ndb.TextProperty(required=True)
	#reference the type of page it is templating, eg league, franchise, rep, team
	label = ndb.StringProperty(required=True)

