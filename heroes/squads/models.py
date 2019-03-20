from google.appengine.ext import ndb
import logging
import os

from heroes import fields
from heroes.models import Base
from heroes.events.models import Event

# for photos
from google.appengine.api import images

class Squad(Base):
    # TEAM IS PARENT
    event = ndb.KeyProperty(kind=Event, required=True)

    photo = ndb.BlobProperty()
    photo_key = ndb.BlobKeyProperty()

    @property
    def publictitle(self):
        return 'a squad title'

    # EVENT stuff
    @property
    def title(self):
        # eg 2016 World Championships
        #TODO: dumb property name
        return self.event.get().title

    @property
    def eventHost(self):
        return self.event.get().hostCity
    

    @property
    def link(self):
        return '/admin/squad/{}/'.format(self.key.urlsafe())

    @property
    def eventdate(self):
        return self.event.get().startdate

    @property
    def teamName(self):
        # eg NZL Elite Men
        return self.key.parent().get().title

    @property
    def divisionName(self):
        #eg Elite Men
        return self.key.parent().get().division.get().title

    @property
    def yearDivision(self):
        #eg 2004 Elite Men
        return str(self.event.get().startdate.year) + " " + self.divisionName
    
    @property
    def publiclink(self):
        return '/squad/{}/'.format(self.key.urlsafe())

    @property
    def photoUrl(self):
        try:
            image_url = images.get_serving_url(self.photo_key)
        except:
            try:
                # Get franchise-specific placeholder image
                # SPORT > COUNTRY > REP
                country = self.key.parent().parent().get()
                sport = country.key.parent().get()
                url = "static/"+sport.code+"/"+country.code+"/img/imgplaceholder-wide.png"
                if os.path.isfile(url):
                    return "/"+url
                else:
                    image_url = "/static/img/placeholder-wide.png"
            except:
                # Catchall
                image_url = "/static/img/placeholder-wide.png"

        return image_url



