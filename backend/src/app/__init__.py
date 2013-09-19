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


import views