from flask import render_template, url_for, request, g, make_response, jsonify
import requests
import json
import sh
import os
import python2platform as p2p

from glob import glob
import magic


from app import app


GIT_SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratch')

GIT_WORKFLOW_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workflowResults')


@app.route('/github', methods=['GET'])
def github():

    
    # Get the organization to be used from the GET
    
    calltype = request.args.get('type','orgs')
    username = request.args.get('username','Data2Semantics')

    
    r = requests.get('https://api.github.com/{}/{}/repos'.format(calltype,username))
    
    repositories = []
    
    
    if r.ok :
        
        repos = json.loads(r.text or r.content)
        
        
        return render_template('github_repositories.html', type=calltype, username=username, repos=repos)
        
        
        
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
            git.clone(clone_url,_cwd=GIT_SCRATCH)
        except Exception:
            
            print "Git repository was already cloned, should pull a new version, but will skip that for now"
            # git.pull(clone_url,_cwd=path)
        
        return jsonify({'name': name, 'path': path})
        
    else :
        return 'error'
    
@app.route('/progress', methods=['GET'])
def progress_bar():
    message = request.args.get('message','Busy...')
    
    return render_template('progress.html',message=message)
  
@app.route('/actions', methods=['GET'])
def actions():
    mimetype = request.args.get('mimetype')
    path = request.args.get('path')
    name = request.args.get('name')
    
    workflows = p2p.applicable(mimetype)
    
    return render_template('actions.html', name=name, path=path, mimetype=mimetype, workflows=workflows)

  
@app.route('/workflow/getList', methods=['GET'])
def get_workflows():
    mimeType = request.args.get('mimeType')
    #mimeType = 'text/turtle'
    
    workflows = p2p.applicable(mimeType)
    
    #realpath = os.path.realpath(__file__)
    #currentDir = os.path.dirname(realpath)
    #files = glob("{}/*".format(currentDir + '/../../../python2platform/data2semantics/python2platform.py'))
    #files = glob("{}/*".format(path))
#     return ', '.join(workflows)
    return jsonify({'results': workflows} )    

@app.route('/workflow/exec')
def execWorkflow():
    workflowId = request.args.get('workflowId')
    filePath = request.args.get('filePath')
    p2p.run(workflowId, GIT_WORKFLOW_RESULTS, filePath)
    return jsonify({'results': True} )
    
    

@app.route('/browse', methods=['GET'])
def browse(path = None):
    if not path :
        path = request.args.get('path')
        
    files = glob("{}/*".format(path))
    
    
    filelist = []
    for p in files:
        (pth, fn) = os.path.split(p)
        
        mimetype = magic.from_file(p, mime=True)
        
        if os.path.isdir(p) :
            filetype = 'dir'
        else :
            filetype = 'file'
        
        print fn, mimetype
        
        filelist.append({'name': fn, 'path': p, 'mimetype': mimetype, 'type': filetype})
    
    
    return render_template('files.html', files=filelist)


