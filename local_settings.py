import webapp2

# ndbadmin settings.
CONFIG = {
    'webapp2_extras.jinja2': {
        'template_path': 'lib/ndbadmin/templates',
        'compiled_path': None,
        'force_compiled': False,
        'environment_args': {
            'autoescape': True,
            'extensions': [
                'jinja2.ext.autoescape',
                'jinja2.ext.with_'
                ]
            },
        'globals': {
            'url_for' : webapp2.uri_for
            },
        'filters': None,
    },
    'webapp2_extras.sessions': {
        'secret_key': 'la-la-la',
    }
}
