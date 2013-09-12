from flask import render_template, url_for, request, g, make_response
import requests
import json
import sh
import os.path
from glob import glob

from app import app

GIT_SCRATCH = '/Users/hoekstra/projects/data2semantics/scratch/'


@app.route('/github/list', methods=['GET'])
def github_list():
    
    # Get the organization to be used from the GET
    
    calltype = request.args.get('type','orgs')
    
    if calltype == 'orgs':
        user = request.args.get('organization','Data2Semantics')
    else :
        user = request.args.get('user','')
    
    r = requests.get('https://api.github.com/{}/{}/repos'.format(calltype,user))
    
    repositories = []
    
    
    if r.ok :
        
        repos = json.loads(r.text or r.content)
        
        
        return render_template('github_repositories.html', repos=repos)
        
        
        
    else :
        return 'error'
    

@app.route('/github/clone', methods=['GET'])
def github_clone():
    clone_url = request.args.get('clone_url',None)
    name = request.args.get('name','test')
    
    if clone_url :
        
        print clone_url
        print name
    
        path = os.path.join(GIT_SCRATCH,name)
        
        print path
        
        git = sh.git.bake(_cwd=GIT_SCRATCH)
        
        try:
            git.clone(clone_url)
        except Exception:
            git.pull(clone_url,_cwd=path)
        
        files = glob("{}/*".format(path))
        
        
        return path
        
    else :
        return 'error'
