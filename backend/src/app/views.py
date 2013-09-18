from flask import render_template, url_for, request, g, make_response, jsonify
import requests
import json
import sh
import os
import python2platform as p2p


from util.dataset import GitDataset
from util.repository import GitHubRepository


from app import app, SCRATCH, WORKFLOW_RESULTS





@app.route('/github', methods=['GET'])
def github():

    
    # Get the organization to be used from the GET
    
    repository_type = request.args.get('type','orgs')
    username = request.args.get('username','Data2Semantics')

    
    try:
        github_repository = GitHubRepository(repository_type, username)
        
        return render_template('github_repositories.html', type=repository_type, username=username, datasets=github_repository.list())

    except Exception as e:
        return e.message
    

    

@app.route('/github/clone', methods=['GET'])
def github_clone():
    clone_url = request.args.get('clone_url',None)
    name = request.args.get('name','test')
    
    if clone_url :
        git_dataset = GitDataset(name)    
        git_dataset.initialize(clone_url)
        
        response = jsonify({'name': name})
        response.set_cookie('repository_name', git_dataset.name)
        
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
    
    workflows = p2p.get_applicable_workflows(mimetype)
    
    return render_template('actions.html', name=name, path=path, mimetype=mimetype, workflows=workflows)

   

@app.route('/workflow/run')
def run_workflow():
    identifier = request.args.get('identifier')
    path = request.args.get('path')
    name = request.args.get('name')
    
    absolute_path = os.path.join(SCRATCH,path)
    
    results_path = os.path.join(os.path.join(WORKFLOW_RESULTS,path),identifier)
    
    p2p.run(identifier, results_path, absolute_path)
    return jsonify({'results': True} )
    
@app.route('/workflow/status')
def get_workflow_status():
    identifier = request.args.get('identifier')
    path = request.args.get('path')
    name = request.args.get('name')
    
    absolute_path = os.path.join(SCRATCH,path)
    
    results_path = os.path.join(os.path.join(WORKFLOW_RESULTS,path),identifier)
    return jsonify({'status': p2p.status(results_path)} )


@app.route('/workflow/provenance')
def upload_workflow_provenance():

    identifier = request.args.get('identifier')
    path = request.args.get('path')
    name = request.args.get('name')

    context = "<http://" + os.path.join(path, name) + ">"
    
    absolute_path = os.path.join(SCRATCH,path)
    results_path = os.path.join(os.path.join(WORKFLOW_RESULTS,path),identifier)
  
    prov_filename = os.path.join(os.path.join(results_path, "prov"),"prov-o.ttl")
    
    prov_file = open(prov_filename, 'r')
    prov_data = prov_file.read()
    prov_file.close()


    headers =  {'content-type':'text/turtle;charset=UTF-8'}
    params = {'context': context}

    r = requests.put('http://semweb.cs.vu.nl:8080/openrdf-sesame/repositories/ct/statements',
                     data = prov_data,
                     params = params,
                     headers = headers)
    
    if r.ok :
        return jsonify({'status': 'true'} )
    else :
        print r
        return jsonify({'status': 'false'})

    


    
@app.route('/browse', methods=['GET'])
def browse():
    print "Browsing"
    path = request.args.get('path', None)
    if not path :
        raise Exception('Must specify a path!')
        
    name = request.args.get('name', request.cookies.get('repository_name'))
    
    print '1', name, path
    
    git_dataset = GitDataset(name)
    
    print '2', name, path
    
    filelist, parent = git_dataset.browse(path)
    
    
    return jsonify({'parent': parent, 'files': filelist})


