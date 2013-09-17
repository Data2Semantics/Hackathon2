from flask import render_template, url_for, request, g, make_response, jsonify
import requests
import json
import sh
import os
import python2platform as p2p


from util.gitrepository import GitRepository


from app import app, SCRATCH, WORKFLOW_RESULTS





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
        git_repo = GitRepository(name)    
        git_repo.initialize(clone_url)
        
        response = jsonify({'name': name})
        response.set_cookie('repository_name', git_repo.name)
        
        return response
    else :
        return 'Error, no clone_url specified'
    
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
    resultsOutput = WORKFLOW_RESULTS + '/' + workflowId + os.path.basename(filePath)
    p2p.run(workflowId, resultsOutput, filePath)
    return jsonify({'results': True} )
    
    

@app.route('/browse', methods=['GET'])
def browse():
    print "Browsing"
    path = request.args.get('path', None)
    if not path :
        raise Exception('Must specify a path!')
        
    name = request.args.get('name', request.cookies.get('repository_name'))
    
    print '1', name, path
    
    git_repo = GitRepository(name)
    
    print '2', name, path
    
    filelist, parent = git_repo.browse(path)
    
    
    return render_template('files.html', files=filelist)


