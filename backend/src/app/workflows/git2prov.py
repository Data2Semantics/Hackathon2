from app import app
import requests
import os
from app.workflows import touch, remove


GIT2PROV_URL = "http://git2prov.org/git2prov"
SERIALIZATION = "PROV-O"
OUTPUT_FILE = "git2prov.ttl"
STATUS_RUNNING = "status.running"
STATUS_FINISHED = "status.finished"
STATUS_ERROR = "status.error"

# ?giturl=https%3A%2F%2Fgithub.com%2Ftdn%2FSMIF-Mozaiek.git&serialization=PROV-O




def run(workflow, source, target):
    
    workflow_identifier = workflow['id']
    
    output_file = os.path.join(target,OUTPUT_FILE)
    
    status_running = os.path.join(target, STATUS_RUNNING)
    status_finished = os.path.join(target, STATUS_FINISHED)
    status_error = os.path.join(target, STATUS_ERROR)
    
    touch(status_running)

    clone_url_path = os.path.join(source,".d2s.url")
    clone_url = open(clone_url_path,'r').read()
    
    app.logger.debug("Calling Git2PROV using clone URL: {}".format(clone_url))
    
    r = requests.get(GIT2PROV_URL, params = {"giturl": clone_url, "serialization": SERIALIZATION})
    
    if r.ok :
        app.logger.debug("Succesfully retrieved provenance trail, writing to {}".format(output_file))
        
        print r.content
        
        open(output_file,'w').write(r.content)
        
        app.logger.debug("Output written to file")
        
        remove(status_running)
        touch(status_finished)
        
    else :
        remove(status_running)
        touch(status_error)
        return False
    
    return True
