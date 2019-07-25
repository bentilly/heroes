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
import cloudstorage
from google.appengine.api import app_identity

class Squadmember(Base):
    #Parent = SQUAD
    rep = ndb.KeyProperty(kind=Rep, required=True)
    role = ndb.KeyProperty(kind=Role)
    position = ndb.KeyProperty(kind=Position)

    photo = ndb.BlobProperty() #not used
    photo_key = ndb.BlobKeyProperty() #used pre June 2019
    # photo_link = ndb.StringProperty(required=False) #file path to image on Cloud Storage (not including bucket)

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
        try:
            #Generate file path
            #get parent objects
            squad_key = self.key.parent()
            team_key = squad_key.parent()
            country_key = team_key.parent()
            sport_key = country_key.parent()
            # file path codes
            sport_code = sport_key.get().code
            country_code = country_key.get().code
            division_code = team_key.get().division.get().code
            squad_code = squad_key.get().code
            #bucket and folder
            bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
            bucket_and_folder = '/'+bucket_name+'/photos/'+sport_code+'/'+country_code+'/'+division_code+'/'+squad_code
            logging.info(bucket_and_folder)
            #file name
            file_name = str(self.title).replace(" ", "-").lower()
            file_name = file_name+'.jpg'


            if bucket_name == "app_default_bucket":
                root_url = 'http://localhost:8080/_ah/gcs'
            else:
                root_url = 'https://storage.googleapis.com'

            image_url = root_url+bucket_and_folder + '/' + file_name

            #check if file exists - this bit will fail if no file
            file = cloudstorage.open(bucket_and_folder + '/' + file_name,'r')
            file.close()

            return image_url

        except:
            logging.info('NO PHOTO IN CLOUD STORAGE')
            try:
                #get_serving_url being blocked by Cloud Storage for any new images. (June 2019)
                image_url = images.get_serving_url(self.photo_key)
                return image_url
            except:
                logging.info('NO PHOTO IN OLD BLOBSTORE')
                return "/static/img/placeholder.png"
                #TODO: a better way of customising placeholder images




        # try:
        #     ###  FIRST: try to get image from old blob store
        #     #get_serving_url being blocked by Cloud Storage for any new images. (June 2019)
        #     image_url = images.get_serving_url(self.photo_key)
        # except:
        #     # this bit is a bit screwy as well...
        #     try:
        #         # Get franchise-specific placeholder image
        #         # SPORT > COUNTRY > REP
        #         country = self.rep.parent().get()
        #         sport = country.key.parent().get()
        #         url = "static/"+sport.code+"/"+country.code+"/img/imgplaceholder.png"
        #         if os.path.isfile(url):
        #             return "/"+url
        #         else:
        #             image_url = "/static/img/placeholder.png"
        #     except:
        #         # Catchall
        #         image_url = "/static/img/placeholder.png"




    # def is_local():
    #     if os.environ.get('SERVER_NAME', '').startswith('localhost'):
    #         return True
    #     elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
    #         return True
    #     else:
    #         return False






    