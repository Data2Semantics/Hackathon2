from flask import render_template, url_for, request, g, make_response
import requests
import json

from app import app



@app.route('/github', methods=['GET'])
def github():
    
    # Get the organization to be used from the GET
    
    calltype = request.args.get('type','orgs')
    
    if calltype == 'orgs':
        user = request.args.get('organization','Data2Semantics')
    else :
        user = request.args.get('user','')
    
    r = requests.get('https://api.github.com/{}/{}/repos'.format(calltype,user))
                     
    return r