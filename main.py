import os

from flask import Flask
from flask import render_template

cur_dir = os.path.abspath(os.path.curdir)

app = Flask(__name__,
            static_folder=os.path.join(cur_dir, 'static'),
            template_folder=os.path.join(cur_dir, 'templates'))
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
