import os
import logging
from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.representatives.models import Rep
from heroes.roles.models import Role
from heroes.positions.models import Position

# for photos
from google.appengine.api import images

class Squadmember(Base):
    #Parent = SQUAD
    rep = ndb.KeyProperty(kind=Rep, required=True)
    role = ndb.KeyProperty(kind=Role)
    position = ndb.KeyProperty(kind=Position)

    photo = ndb.BlobProperty()
    photo_key = ndb.BlobKeyProperty()

    @property
    def replink(self):
        rep_uid = self.rep.get().uid
        if rep_uid:
            return '/rep/{}/'.format(self.rep.get().uid)
        else:
            # if no uid, return key
            return self.rep.get().publiclink

    @property
    def publiclink(self):
        return '/sm/{}/'.format(self.key.urlsafe())

    @property
    def title(self):
        return self.rep.get().firstname + " " + self.rep.get().lastname

    @property
    def link(self):
        return '/admin/squadmember/{}/'.format(self.key.urlsafe())

    @property
    def roleName(self):
            return self.role.get().name

    @property
    def positionName(self):
            return self.position.get().name

    @property
    def photoUrl(self):
        # photo
        try:
            image_url = images.get_serving_url(self.photo_key)
        except:
            try:
                # Get franchise-specific placeholder image
                # SPORT > COUNTRY > REP
                country = self.rep.parent().get()
                sport = country.key.parent().get()
                url = "static/"+sport.code+"/"+country.code+"/img/imgplaceholder.png"
                if os.path.isfile(url):
                    return "/"+url
                else:
                    image_url = "/static/img/placeholder.png"
            except:
                # Catchall
                image_url = "/static/img/placeholder.png"

        return image_url







    