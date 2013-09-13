from flask import render_template, url_for, request, g, make_response, jsonify
import requests
import json
import sh
import os
from glob import glob
import mimetypes

from app import app


GIT_SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratch')

@app.route('/github/list', methods=['GET'])
def github_list():
    
    # Get the organization to be used from the GET
    
    calltype = request.args.get('type','orgs')
    
    if calltype == 'orgs':
        user = request.args.get('user','Data2Semantics')
    else :
        user = request.args.get('user','')
    
    r = requests.get('https://api.github.com/{}/{}/repos'.format(calltype,user))
    
    repositories = []
    
    
    if r.ok :
        
        repos = json.loads(r.text or r.content)
        
        
        return render_template('github_repositories.html', user=user, repos=repos)
        
        
        
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
        
        return browse(path)
        
    else :
        return 'error'
    
@app.route('/progress', methods=['GET'])
def progress_bar():
    message = request.args.get('message','Busy...')
    
    return render_template('progress.html',message=message)
    
@app.route('/browse', methods=['GET'])
def browse(path = None):
    if not path :
        path = request.args.get('path')
        
    files = glob("{}/*".format(path))
    
    mimetypes.init()
    
    filelist = []
    for p in files:
        (pth, fn) = os.path.split(p)
        (mimetype,e) = mimetypes.guess_type(p)
        
        if os.path.isdir(p) :
            filetype = 'dir'
        else :
            filetype = 'file'
        
        filelist.append({'name': fn, 'path': p, 'mime': mimetype, 'type': filetype})
    
    
    return jsonify({'results': filelist} )    


