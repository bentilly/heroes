from flask import render_template, redirect, url_for

from heroes import create_app


app = create_app()
#NEXT heroes/__init__.py

# @app.route('/')
# def index():
#     return redirect('/sport/all')

@app.route('/admin')
def index():
    return redirect('admin/sport/all')
#NEXT heroes/__init__.py

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
