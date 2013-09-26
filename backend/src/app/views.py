from flask import render_template, url_for, request, g, make_response, jsonify, session
import requests
import json
import sh
import os
import workflows

from util.dataset import GitDataset
from util.repository import GitHubRepository


from app import app, SCRATCH





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
    dataset = request.args.get('dataset')
    
    actions = workflows.get_workflows(mimetype)
    
    response = {'dataset': dataset, 'name': name, 'path': path, 'mimetype': mimetype, 'workflows': actions}
    
    return jsonify(response)

   

@app.route('/workflow/run')
def run_workflow():
    workflow_identifier = request.args.get('workflow_id')
    filepath = request.args.get('filepath')
    dataset_name = request.args.get('dataset')

    
    source = workflows.run(workflow_identifier, dataset_name, filepath)
    
    return jsonify({'running': True,'workflow_id': workflow_identifier, 'source': source, 'dataset': dataset_name} );
    
@app.route('/workflow/status')
def get_workflow_status():
    workflow_id = request.args.get('workflow_id')
    filepath = request.args.get('filepath')
    
    app.logger.debug("Checking workflow status for {}".format(workflow_id))
    
    return jsonify({'status': workflows.status(workflow_id, filepath), 'workflow_id': workflow_id, 'filepath': filepath} )


@app.route('/workflow/provenance')
def upload_workflow_provenance():

    identifier = request.args.get('identifier')
    path = request.args.get('path')
    name = request.args.get('name')

    context = "<http://" + os.path.join(path, name) + ">"
    
    absolute_path = os.path.join(SCRATCH,path)
    results_path = os.path.join(os.path.join(workflows.WORKFLOW_RESULTS,path),identifier)
  
    prov_filename = os.path.join(os.path.join(results_path, "prov"),"prov-o.ttl")
    
    prov_file = open(prov_filename, 'r')
    prov_data = prov_file.read()
    prov_file.close()

    headers =  {'content-type':'text/turtle;charset=UTF-8'}
    params = {'context': context}

    r = requests.put('http://semweb.cs.vu.nl:8080/openrdf-sesame/repositories/goldendemo/statements',
                     data = prov_data,
                     params = params,
                     headers = headers)
    
    if r.ok :
        return jsonify({'status': 'true'} )
    else :
        return jsonify({'status': 'false'})

    


    
@app.route('/browse', methods=['GET'])
def browse():
    path = request.args.get('path', None)
    if not path :
        raise Exception('Must specify a path!')
        
    name = request.args.get('name', request.cookies.get('repository_name'))
    
    git_dataset = GitDataset(name)

    filelist, parent = git_dataset.browse(path)
    
    
    return jsonify({'parent': parent, 'files': filelist})


