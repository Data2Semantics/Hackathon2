from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy

import os

# Make sure we have an absolute path to the template dir
TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratch')

# STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Intialize the Flask Appliation
app = Flask(__name__, template_folder = TEMPLATE_FOLDER)
app.debug = True

app.secret_key = 'jedenkttochzekernietdatjedezesecretkeykanradenhe?'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goldendemo.db'
#db = SQLAlchemy(app)
#
#if not os.path.exists('goldendemo.db'):
#    app.logger.warn("Database does not exist, will create one")
#    db.create_all()


## JINJA2 Filters
_base_js_escapes = (
    ('\\', r'\u005C'),
    ('\'', r'\u0027'),
    ('"', r'\u0022'),
    ('>', r'\u003E'),
    ('<', r'\u003C'),
    ('&', r'\u0026'),
    ('=', r'\u003D'),
    ('-', r'\u002D'),
    (';', r'\u003B'),
    ('/', '_'), # Added by RH
    (' ', '_'), # Added by RH
    ('.', '_'), # Added by RH
    (u'\u2028', r'\u2028'),
    (u'\u2029', r'\u2029')
)

# Escape every ASCII character with a value less than 32.
_js_escapes = (_base_js_escapes +
               tuple([('%c' % z, '\\u%04X' % z) for z in range(32)]))

# escapejs from Django: https://www.djangoproject.com/
@app.template_filter('escapejs')
def escapejs(value):
    """Hex encodes characters for use in JavaScript strings."""
    if not isinstance(value, basestring):
        value = str(value)

    for bad, good in _js_escapes:
        value = value.replace(bad, good)

    return value



import views