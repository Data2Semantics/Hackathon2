from flask import Flask
import os

# Make sure we have an absolute path to the template dir
TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


# STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Intialize the Flask Appliation
app = Flask(__name__, template_folder = TEMPLATE_FOLDER)



app.debug = True

import views