import webapp2

from ndbadmin import settings
from ndbadmin import urls


app = webapp2.WSGIApplication(urls.urlpatterns,
                              debug=settings.DEBUG, config=settings.CONFIG)
