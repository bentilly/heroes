import logging
import os
import jinja2
import cloudstorage
import webapp2

from google.appengine.api import app_identity
from flask import Blueprint, render_template, redirect, request

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)
GCS_BUCKET = '/dev-sports-heroes.appspot.com'


class BaseHandler(webapp2.RequestHandler):

	def write(self, *a, **kw):
		return self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		return self.write(self.render_str(template, **kw))

	def render_template(self, view_filename, params=None):
		if params is None:
			params = {}
			template = jinja_env.get_template(view_filename)
			return self.response.out.write(template.render(params))


class MainPage(BaseHandler):
	def get(self):
		return self.render_template("gcs.html")


class UploadFileHandler(BaseHandler):
	def post(self):

		if self.request.get('uploaded-file'):
			uploaded_file = self.request.POST.get('uploaded-file')
			file_content = uploaded_file.file.read()

			# NAME
			#remove spaces
			file_name = str(uploaded_file.filename).replace(" ", "-")
			# TODO: enforce file extension, check for file already existing etc
			# file_name = str(uploaded_file.filename).replace(" ", "-").replace(".", "-")

			# TYPE
			file_type = uploaded_file.type
			# Assume for now file_name includes extension
			# file_name += "." + file_type.split("/")[1]  # if type is image/png, add .png at the end

			# upload the file to Google Cloud Storage
			gcs_file = cloudstorage.open(
				GCS_BUCKET + '/' + file_name,
				'w',
				content_type=file_type,
				retry_params=cloudstorage.RetryParams(backoff_factor=1.1)
				)

			gcs_file.write(file_content)
			gcs_file.close()


			# get the URL
			url = 'http://localhost:8080/_ah/gcs' if is_local() else 'https://storage.googleapis.com'
			url += GCS_BUCKET + '/' + file_name

			logging.info('++++++++++++++===============')
			logging.info(url)
			return self.render_template("gcss.html")
		else:
			logging.info('>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')
			return self.error(400)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainPage),
    webapp2.Route('/upload', UploadFileHandler),
], debug=True)



def is_local():
    """ Check if you are currently running on localhost or on GAE. """
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False









