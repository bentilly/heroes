from google.appengine.ext import ndb
import logging
import os

from heroes import fields
from heroes.models import Base
from heroes.events.models import Event

# for photos
from google.appengine.api import images
import cloudstorage
from google.appengine.api import app_identity

class Squad(Base):
    # TEAM IS PARENT
    event = ndb.KeyProperty(kind=Event, required=True)
    code = ndb.StringProperty(required=False) #uid for this squad. Enables multiple squads in a year

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
            #Generate file path
            #get parent objects
            team_key = self.key.parent()
            country_key = team_key.parent()
            sport_key = country_key.parent()
            # file path codes
            sport_code = sport_key.get().code
            country_code = country_key.get().code
            division_code = team_key.get().division.get().code
            squad_code = self.code
            #bucket and folder
            bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
            bucket_and_folder = '/'+bucket_name+'/photos/'+sport_code+'/'+country_code+'/'+division_code+'/'+squad_code
            logging.info(bucket_and_folder)
            #file name
            file_name = squad_code+'-'+country_code+'-'+division_code
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
                return "/static/img/placeholder-wide.png"
                #TODO: a better way of customising placeholder images





